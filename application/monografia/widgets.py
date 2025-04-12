from django.forms.widgets import ClearableFileInput

class CustomClearableFileInput(ClearableFileInput):
    initial_text = "Arquivo Atual"
    input_text = "Selecionar novo arquivo"               
    clear_checkbox_label = "Remover"      
