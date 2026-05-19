import torch
import torch.nn as nn
import os
from torch.utils.data import DataLoader
from torchinfo import summary


class Trainer:
    def __init__(self,
                 model: nn.Module,
                 optimizer: torch.optim.Optimizer,
                 loss_fn: nn.Module,
                 device: str = None,
                 out_dir: str = None,
                 use_notebook: bool = False, ):
        self.device = device if device is not None else ("cuda" if torch.cuda.is_available() else "cpu")

        self.model = model
        self.model.to(self.device)

        self.loss_fn = loss_fn
        self.optimizer = optimizer

        self.do_save = False if out_dir is None else True
        self.out_dir = out_dir

        self.current_epoch = 0
        self.best_metric = - float('inf')
        self.history = {'train_acc': [], 'train_loss': [], 'val_acc': [], 'val_loss': []}

        if self.do_save:
            os.makedirs(self.out_dir, exist_ok=True)

        self.tqdm = __import__('tqdm.notebook' if use_notebook else 'tqdm', fromlist=['tqdm']).tqdm

    def summary(self, input_size):
        return summary(self.model, input_size=input_size)

    def train_step(self, batch):
        """Override this for custom training logic."""
        inputs, labels = batch
        inputs, labels = inputs.to(self.device), labels.to(self.device)

        self.optimizer.zero_grad()
        outputs = self.model(inputs)
        loss = self.loss_fn(outputs, labels)
        loss.backward()
        self.optimizer.step()

        _, preds = outputs.max(1)
        correct = preds.eq(labels).sum().item()

        return {'loss': loss.item(), 'correct': correct, 'total': labels.size(0)}

    def validate_step(self, batch):
        """Override this for custom validation logic."""
        inputs, labels = batch

        with torch.no_grad():
            inputs, labels = inputs.to(self.device), labels.to(self.device)

            outputs = self.model(inputs)
            loss = self.loss_fn(outputs, labels)
            _, preds = outputs.max(1)
            correct = preds.eq(labels).sum().item()

        return {'loss': loss.item(), 'correct': correct, 'total': labels.size(0)}

    def fit(self,
            train_loader: DataLoader,
            val_loader: DataLoader,
            epochs: int = 10):

        epoch_pbar = self.tqdm(range(epochs), desc="Training", unit="epoch")

        for epoch in epoch_pbar:
            self.current_epoch = epoch + 1

            # Training
            self.model.train()
            train_loss, train_correct, train_total = 0, 0, 0
            for batch in train_loader:
                result = self.train_step(batch)
                train_loss += result['loss']
                train_correct += result['correct']
                train_total += result['total']
            train_loss /= len(train_loader)
            train_acc = 100 * train_correct / train_total if train_total > 0 else 0

            # Validation
            self.model.eval()
            val_loss, val_correct, val_total = 0, 0, 0
            for batch in val_loader:
                result = self.validate_step(batch)
                val_loss += result['loss']
                val_correct += result.get('correct', 0)
                val_total += result.get('total', 0)
            val_loss /= len(val_loader)
            val_acc = 100 * val_correct / val_total if val_total > 0 else 0

            # Track history
            self.history['train_acc'].append(train_acc)
            self.history['train_loss'].append(train_loss)
            self.history['val_acc'].append(val_acc)
            self.history['val_loss'].append(val_loss)

            # Logging
            epoch_pbar.set_postfix(
                train_acc=f"{train_acc:.2f}%",
                train_loss=f"{train_loss:.4f}",
                val_acc=f"{val_acc:.2f}%",
                val_loss=f"{val_loss:.4f}",
            )
            # Checkpointing
            if self.do_save and val_acc > self.best_metric:
                self.best_metric = val_acc
                self.save_checkpoint()
                self.tqdm.write(f"Best model saved (acc: {val_acc:.2f}%)")

        return self.history

    def save_checkpoint(self, filename: str = None):
        if filename is None:
            filename = f"checkpoint_epoch_{self.current_epoch}.pth"
        filepath = os.path.join(self.out_dir, filename)
        torch.save({
            'epoch': self.current_epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'best_metric': self.best_metric,
            'history': self.history,
        }, filepath)

    def load_checkpoint(self, filepath: str):
        checkpoint = torch.load(filepath, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.current_epoch = checkpoint['epoch']
        self.best_metric = checkpoint['best_metric']
        self.history = checkpoint['history']
        return checkpoint

    def evaluate(self, test_loader: DataLoader):
        """Standalone evaluation on test set."""
        self.model.eval()
        test_loss, correct, total = 0, 0, 0

        with torch.no_grad():
            for batch in test_loader:
                result = self.validate_step(batch)
                test_loss += result['loss']
                correct += result.get('correct', 0)
                total += result.get('total', 0)

        test_loss /= len(test_loader)
        test_acc = 100 * correct / total if total > 0 else 0

        print(f'Test Loss: {test_loss:.4f}, Test Accuracy: {test_acc:.2f}%')
        return test_loss, test_acc
