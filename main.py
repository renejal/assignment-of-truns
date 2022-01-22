from views.general_shift_view import GenerateShiftView
from conf.settings import JSON_SITES_DATA, JSON_VIGILANTES_DATA

view = GenerateShiftView(JSON_SITES_DATA,JSON_VIGILANTES_DATA)
view.execute()
