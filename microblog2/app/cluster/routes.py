from flask import render_template, flash, redirect, url_for, request
#from werkzeug.urls import url_parse
from app import db
from app.cluster.forms import ClusterCreationForm
from flask_login import login_required
from app.cluster import bp
from app.models import Cluster


# ...
#@app.route('/')
#@app.route('/index', methods=['GET', 'POST'])
#def index():
#    return render_template('index.html')

#### still pending...
@bp.route('/cluster', methods=['GET', 'POST'])
@login_required
def cluster():
    #if current_user.is_authenticated:
    #    return redirect(url_for('cluster.cluster'))
    form = ClusterCreationForm()
    if form.validate_on_submit():
        cluster = Cluster(cluster_name=form.cluster_name.data, description=form.description.data,cluster_type=form.cluster_type.data, cluster_os=form.cluster_os.data, node_count=form.node_count.data)
        db.session.add(cluster)
        db.session.commit()
        flash('Cluster has been created!!')
        return redirect(url_for('main.index'))
    return render_template('cluster/cluster.html', title='cluster', form=form)
