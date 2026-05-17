#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <locale.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

#include "VibeAlgorithm.h"

namespace py = pybind11;


// НАЗВАНИЕ МОДУЛЯ!!!
PYBIND11_MODULE(VibeExtractor, m, py::mod_gil_not_used()) {
    std::setlocale(LC_ALL, "Russian");

    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: VibeExtractor

        .. autosummary::
           :toctree: _generate

           VibeAlgorithm
    )pbdoc";



    // Название и ссылка на функцию
    py::class_<VibeAlgorithm>(m, "VibeAlgorithm")
        .def(py::init<py::array_t<uint8_t>, int, int, int, int>(),
            py::arg("image"),
            py::arg("N"),
            py::arg("R"),
            py::arg("_min"),
            py::arg("phi"),
            "Constructs a ViBeAlgorithm instance.\n\n"
            "Args:\n"
            "    image (ndarray): The initial single color channel image.\n"
            "    N (int): The value for vibe N parameter.\n"
            "    R (int): The value for vibe R parameter.\n"
            "    _min (int): The value for vibe #min parameter.\n"
            "    phi (int): The value for vibe phi parameter."
        )
        .def("vibe_detection", &VibeAlgorithm::vibe_detection, py::arg("image"),
            "Provides the motion mask for the given image. \n"
            "Args:\n"
            "   image (ndarray): The single color channel image to be processed."
        )
        ;

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
