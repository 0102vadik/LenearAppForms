import tkinter as tk
from tkinter import ttk
import LinearService as service
from tkinter.messagebox import showerror

class RootForm(tk.Toplevel):
    def __init__(self, parent, numberVariables, numberRestrictions):
        super().__init__(parent)

        label = tk.Label(self, text="Коэффициенты ЦФ", justify='left')
        label.grid(row=0, columnspan=2)

        label = tk.Label(self, text="Напр.", justify='left')
        label.grid(row=0, column=numberVariables*2)

        self.objectiveFunctionCoefficients = []
        for i in range(1):
            self.objectiveFunctionCoefficient = []
            for j in range(numberVariables):
                entry = tk.Entry(self)
                entry.grid(row=1, column=j * 2)
                if (j != numberVariables - 1):
                    label = tk.Label(self, text="x{} + ".format(j + 1))
                else:
                    label = tk.Label(self, text="x{}".format(j + 1))
                label.grid(row=1, column=j * 2 + 1)
                self.objectiveFunctionCoefficient.append((entry, label))

            self.objectiveFunctionDirection = tk.StringVar()
            combobox = ttk.Combobox(self, values=["min", "max"], textvariable=self.objectiveFunctionDirection)
            combobox.grid(row=1, column=numberVariables*2)
            self.objectiveFunctionCoefficients.append(self.objectiveFunctionCoefficient)

        label = tk.Label(self, text="Коэффициенты огран-й", justify='left')
        label.grid(row=2, columnspan=2)

        label = tk.Label(self, text="Знак", justify='left')
        label.grid(row=2, column=numberVariables * 2)

        label = tk.Label(self, text="Правая часть", justify='left')
        label.grid(row=2, column=numberVariables * 2 + 1)

        self.restrictions = []
        for i in range(numberRestrictions):
            self.restriction = []
            for j in range(numberVariables):
                entry = tk.Entry(self)
                entry.grid(row=i + 3, column=j * 2)
                if (j != numberVariables - 1):
                    label = tk.Label(self, text="x{} + ".format(j + 1))
                else:
                    label = tk.Label(self, text="x{}".format(j + 1))
                label.grid(row=i + 3, column=j * 2 + 1)
                self.restriction.append((entry, label))

            equal_combobox = ttk.Combobox(self, values=["=", "<=", ">="])
            equal_combobox.grid(row=i + 3, column=numberVariables*2)
            entry = tk.Entry(self)
            entry.grid(row=i + 3, column=numberVariables*2+1)
            self.restriction.append((entry, equal_combobox))
            self.restrictions.append(self.restriction)

        button = tk.Button(self, text="Рассчитать", command=self.get_table_data)
        button.grid(row=999, columnspan=numberVariables*3)


    def get_table_data(self):

        self.data = []

        self.objectiveFunction_data = []
        for self.objectiveFunction in self.objectiveFunctionCoefficients:
            for self.entry, self.label in self.objectiveFunction:
                self.objectiveFunction_data.append(self.entry.get())
            self.objectiveFunction_data.append(self.objectiveFunctionDirection.get())

        self.restriction_all_data = []
        for self.restriction in self.restrictions:
            self.restriction_data = []
            for self.entry, self.label in self.restriction:
                self.restriction_data.append(self.entry.get())
            self.restriction_data.append(self.restriction[-1][1].get())
            self.restriction_all_data.append(self.restriction_data)

        self.data.append((self.objectiveFunction_data, self.restriction_all_data))
        PARAM = service.start(self.objectiveFunction_data, self.restriction_all_data)

        objectiveFunctionResult = PARAM.fun
        internalParametersResults = PARAM.x
        ResultForm(self, objectiveFunctionResult, internalParametersResults)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.numberVariables = tk.StringVar()
        self.numberRestrictions = tk.StringVar()

        label1 = tk.Label(self, text="Количество переменных:")
        label1.grid(row=0, columnspan=2)
        combobox1 = ttk.Combobox(self, values=["2", "3", "4", "5", "6", "7", "8", "9", "10"], textvariable=self.numberVariables)
        combobox1.current(0)
        combobox1.grid(row=1, column=0)

        label2 = tk.Label(self, text="Количество ограничений:")
        label2.grid(row=2, columnspan=2)
        combobox2 = ttk.Combobox(self, values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], textvariable=self.numberRestrictions)
        combobox2.current(0)
        combobox2.grid(row=3, column=0)

        a = tk.Button(self, text="Далее", command=self.open_window)
        a.grid(row=4, column=0)

    def open_window(self):
        if self.numberVariables.get() != '' or int(self.numberVariables.get()) > 0:
            if self.numberRestrictions.get() != '' or int(self.numberRestrictions.get()) > 0:
                RootForm(self, int(self.numberVariables.get()), int(self.numberRestrictions.get()))
            else:
                tk.messagebox.showerror(title='Ошибка', message='Количество ограничений должно быть больше нуля')
        else:
            tk.messagebox.showerror(title='Ошибка', message='Количество переменных должно быть больше единицы')

class ResultForm(tk.Toplevel):
    def __init__(self, parent, objectiveFunctionResult, internalParametersResults):
        super().__init__(parent)
        label = tk.Label(self, text="Значение ЦФ:", justify='left')
        label.grid(row=0, column=1)

        label = tk.Label(self, text=f"{objectiveFunctionResult}", justify='left')
        label.grid(row=1, column=1)

        label = tk.Label(self, text="Значения внутренних параметров:", justify='left')
        label.grid(row=2, column=1)

        rows = 3
        i = 1
        for internalParameterResult in internalParametersResults:
            internalParameterResultLabel = tk.Label(self, text=f"x{i}: {internalParameterResult}", justify='left')
            internalParameterResultLabel.grid(row=rows, columnspan=2)
            rows = rows + 1
            i = i + 1

        button = tk.Button(self, text="Закрыть", command=self.close)
        button.grid(row=999, columnspan=2)

    def close(self):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()