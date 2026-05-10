#include <pybind11/pybind11.h>
#include <pybind11/numpy.h> // Вот тут
#include <pybind11/embed.h>
#include <ctime>
#include <cstdint>

namespace py = pybind11;


// .h файл с кодом на c++
// Поскольку тутвведется работа с массивами numpy, подключает соответствующую библиотеку ^
class VibeAlgorithm
{
private:
	int param_N;
	int param_R;
	int param_min;
	int param_phi;

	uint8_t*** samples;
	size_t height;
	size_t width;
	size_t depth;


// И тут нужно небольшое отступление...

/* Дело в том, что массивы numpy хранятся не совсем как обычные массивы. При обращении к массиву мы на самом деле
обращаемся к "буферу" (скорее заголовку/оглавлению, но он зовется буфером. Он содержит:
- Размерность массива (его измерения),
- Размер массива (число элементов),
- Минимальное и максимальное значение,
- Тип данных,
- И указатель на структуру, содержащую наши данные (причем в этих данных могут быть пробелы (strides - шаги) и разная
 адресация (c или Fortran), и это тоже нужно учитывать).
*/
	
public:
    // Поскольку в массиве могут быть пробелы или структура, при получении нового массива в функцию (метод) указываем
    // стиль адресации (c_style или f_style) и приводим массив к сплошным значениям
	VibeAlgorithm(py::array_t<uint8_t, py::array::c_style | py::array::forcecast> image, int N, int R, int _min, int phi)
	{
		std::srand((unsigned)std::time(0));

		this->param_N = N;
		this->param_R = R;
		this->param_min = _min;
		this->param_phi = phi;


		py::buffer_info buf_image = image.request();
		uint8_t* ptr_image = (uint8_t*)buf_image.ptr;
		this->height = buf_image.shape[0];
		this->width = buf_image.shape[1];
		this->depth = N;

		
		this->samples = new uint8_t **[this->height]();
		for (size_t i = 0; i < this->height; ++i)
		{
			this->samples[i] = new uint8_t * [this->width]();
			for (size_t j = 0; j < this->width; ++j)
			{
				this->samples[i][j] = new uint8_t[N]();
			}
		}

		for (size_t i = 0; i < this->height; ++i)
		{
			for (size_t j = 0; j < this->width; ++j)
			{
				for (size_t n = 0; n < N; ++n)
				{
					int x = 0;
					int y = 0;
					while (x == 0 && y == 0)
					{
						x = (std::rand() % 3) - 1;
						y = (std::rand() % 3) - 1;
					}
					int ri = i + x;
					int rj = j + y;

					if (ri >= 0 && rj >= 0 && ri < this->height && rj < this->width)
					{
						this->samples[i][j][n] = ptr_image[ri * this->width + rj];
					}
					
				}
			}
		}
	}

	py::array_t<uint8_t> vibe_detection(py::array_t<uint8_t, py::array::c_style | py::array::forcecast> image)
	{
		std::srand((unsigned)std::time(0));


		py::buffer_info buf_image = image.request();
		uint8_t* ptr_image = (uint8_t*)buf_image.ptr;

		py::array_t<uint8_t> segmap = py::array_t<uint8_t>(this->height * this->width);
		py::buffer_info buf_segmap = segmap.request();
		uint8_t* ptr_segmap = (uint8_t*)buf_segmap.ptr;
		size_t total_size = this->height * this->width * sizeof(uint8_t);
		std::memset(ptr_segmap, 0, total_size);

		for (size_t i = 0; i < this->height; ++i)
		{
			for (size_t j = 0; j < this->width; ++j)
			{
				int count = 0;
				int index = 0;
				int dist = 0;

				while (count < this->param_min && index < this->param_N)
				{
					dist = std::abs((int) ptr_image[i * this->width + j] - this->samples[i][j][index]);
					if (dist < this->param_R)
					{
						++count;
					}
					++index;
				}

				if (count >= this->param_min)
				{
					int r = std::rand() % (this->param_N);
					if (!r)
					{
						r = std::rand() % (this->param_N);
						this->samples[i][j][r] = ptr_image[i * this->width + j];
					}

					r = std::rand() % (this->param_N);
					if (!r)
					{
						int x = 0;
						int y = 0;
						while (x == 0 && y == 0)
						{
							x = (std::rand() % 3) - 1;
							y = (std::rand() % 3) - 1;
						}
						r = std::rand() % (this->param_N);

						int ri = i + x;
						int rj = j + y;
						if (ri >= 0 && rj >= 0 && ri < this->height && rj < this->width)
						{
							this->samples[ri][rj][r] = ptr_image[i * this->width + j];
						}
					}
				}
				else
				{
					ptr_segmap[i * this->width + j] = 255;
				}
			}
		}
		segmap.resize({ this->height, this->width });

		return segmap;
	}

	~VibeAlgorithm()
	{
		for (size_t i = 0; i < this->height; ++i)
		{
			for (size_t j = 0; j < this->width; ++j)
				delete[] this->samples[i][j];
			delete[] this->samples[i];
		}
		delete[] this->samples;
	}
};


