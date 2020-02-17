from flask_wtf import Form
#, validators
from wtforms import StringField, BooleanField, SubmitField, SelectField, IntegerField, FormField
from wtforms.validators import ValidationError, DataRequired, Length, NumberRange
from app.models import Cluster


class ClusterCreationForm(Form):
    cluster_name = StringField('Name', validators=[DataRequired(),Length(max=50)])
    description = StringField('Description', [Length(max=200)])
    cluster_type = SelectField(u'Cluster Type', choices=[('openstack', 'openstack'), ('AWS', 'AWS'), ('baremetal', 'baremetal')])
    cluster_os = SelectField(u'Cluster OS', choices=[('centos', 'centos'), ('ubuntu', 'ubuntu')])
    node_count = IntegerField('node count', default=4)
        #FormField(NumberRange(min=1, max=100, message="value must be integer between 1 to 100"))
#BooleanField('node_count', validators=[DataRequired(),NumberRange(min=1, max=100, message="range of count can be 1 to 100")])
    submit = SubmitField('Create Cluster')

    def validate_name(self, cluster_name):
        cluster = Cluster.query.filter_by(cluster_name=cluster_name.data).first()
        if cluster is not None:
            raise ValidationError('Please use a different cluster name.')