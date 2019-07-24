from customclasses import MyGrid
from customclasses import SectionLabel
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button


class Add_Talent_Button(Button):
    def __init__(self, **kwargs):
        super(Add_Talent_Button, self).__init__(**kwargs)
        self.text = "DODAJ KURWA"


class SkillsBox(MyGrid):
    def __init__(self, **kwargs):
        super(SkillsBox, self).__init__(**kwargs)


class SkillsLabel(Label):
    def __init__(self, **kwargs):
        super(SkillsLabel, self).__init__(**kwargs)
        self.text = "Umiejętności"


class TalentsLabel(Label):
    def __init__(self, **kwargs):
        super(TalentsLabel, self).__init__(**kwargs)
        self.text = "Talenty"


class SkillsSection(SectionLabel):
    def __init__(self, **kwargs):
        super(SkillsSection, self).__init__(**kwargs)
        self.text = "Talenty i Umiejętności"


class TalentGrid(MyGrid):
    def __init__(self, **kwargs):
        super(TalentGrid, self).__init__(**kwargs)


class SkillsGrid(MyGrid):
    def __init__(self, **kwargs):
        super(SkillsGrid, self).__init__(**kwargs)
