from marshmallow import fields
from settings.ma import ma


class CodeSchema(ma.Schema):
    language = fields.String()
    content = fields.String()


class ImageSchema(ma.Schema):
    url = fields.URL()
    description = fields.String()


class ContentSchema(ma.Schema):
    paragraph_title = fields.String(required=True)
    content = fields.String(required=True)
    code = ma.Nested(CodeSchema)
    image = ma.Nested(ImageSchema)
