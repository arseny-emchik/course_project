class BaseGUI:
    def _getTextTitle(self, algorithm, file_path):
        text = 'New win has been created!\n'
        text += 'Params:\n'
        text += 'Algorithms: ' + algorithm + "\n"
        text += 'Data set path: ' + file_path + "\n"
        return text

    def _getStr(self, num_float, precision=4):
        return str(round(num_float, precision))

    def _clearTextView(self, builder):
        entryForText = builder.get_object('main_text_view')
        entryForText.get_buffer().set_text('')

    def _showText(self, builder, line):
        self._clearTextView(builder)
        entryForText = builder.get_object('main_text_view')

        line += '\n=====================================\n'
        entryForText.get_buffer().insert(entryForText.get_buffer().get_end_iter(), line)