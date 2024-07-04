import warnings

import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        self._listYear=self._model._allYears

        for a in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(a))
        self._view.update_page()
    def fillDDShapes(self, e):
        anno=self._view.ddyear.value
        shapes = DAO.getAllShapes(anno)
        for shape in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(shape))
        self._view.update_page()
    def handle_graph(self, e):
        """
        xG = self._view.txtXG.value
        try:
            intXG = int(xG)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, soglia inserita non numerica"))
            self._view.update_page()
            return
        if intXG >180 or intXG <1:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire in xG un numero compreso tra 1 e 180 "))
            self._view.update_page()
            return
        """

        a = self._view.ddyear.value
        s = self._view.ddshape.value

        self._model.buildGraph(a, s)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(
            f"Numero di vertici: {self._model.getNumNodi()} Numero di archi: {self._model.getNumArchi()}"
        ))
        """
        for p in self._model.getSumWeightNeigh():
            self._view.txt_result.controls.append(ft.Text(f"Nodo {p[0]}, somma pesi su archi ={p[1]}"))
        """

        self._view.update_page()

    def handle_path(self, e):
        path, pesoBest = self._model.computePath()

        self._view.txtOut2.controls.append(ft.Text(
            f"Peso cammino massimo: {pesoBest}"))

        for p in path:
            self._view.txtOut2.controls.append(ft.Text(
                f"{p[0].id} --> {p[1].id}: weight {p[2]} distance {str(self._model.get_distance_weight(p))}"))

        self._view.update_page()