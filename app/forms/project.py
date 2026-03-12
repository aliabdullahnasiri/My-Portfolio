from wtforms import (
    BooleanField,
    DateField,
    FileField,
    HiddenField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
    URLField,
)
from wtforms.validators import URL, DataRequired, Length, Optional

from app.forms import Form


class AddProjectForm(Form):

    profile_uid = StringField("Profile UID", validators=[DataRequired()])

    title = StringField("Project Title", validators=[DataRequired(), Length(max=150)])

    short_description = TextAreaField(
        "Short Description", validators=[Optional(), Length(max=300)]
    )

    description = TextAreaField("Full Description", validators=[Optional()])

    github_url = URLField("GitHub Repository", validators=[Optional(), URL()])

    demo_url = URLField("Live Demo", validators=[Optional(), URL()])

    documentation_url = URLField("Documentation", validators=[Optional(), URL()])

    project_type = SelectField(
        "Project Type",
        choices=[
            ("web", "Web Application"),
            ("tool", "Security Tool"),
            ("script", "Script"),
            ("research", "Research"),
        ],
        validators=[Optional()],
    )

    status = SelectField(
        "Project Status",
        choices=[
            ("completed", "Completed"),
            ("ongoing", "Ongoing"),
        ],
        validators=[Optional()],
    )

    start_date = DateField("Start Date", validators=[Optional()])
    end_date = DateField("End Date", validators=[Optional()])

    display_order = IntegerField("Display Order", validators=[Optional()])

    cover = FileField("Cover Image")

    technologies = StringField("Technologies", validators=[Optional()])

    submit = SubmitField("Add")


class UpdateProjectForm(AddProjectForm):
    uid = HiddenField("UID", validators=[DataRequired()])

    is_featured = BooleanField("Show this item as Featured")
    is_public = BooleanField("Make this item Publicly Visible")

    submit = SubmitField("Update")
