@app.route('/data/power')
def DataPower():
    if request.method == 'GET':
        stats = NodePowerStatModel.query.all()
        icpes = iCPEModel.query.all()
        return render_template('data/power.html', icpes = icpes)

@app.route('/data/power/<mac>')
def DataPoweriCPE(mac):
    if request.method == 'GET':
        icpe = iCPEModel.query.filter_by(mac = mac).first()
        return render_template('data/powericpe.html', icpe = icpe)


@app.route('/data/power/<mac>/<nodeid>')
def DataPoweriCPENode(mac, nodeid):
    if request.method == 'GET':
        icpe = iCPEModel.query.filter_by(mac = mac).first()
        return render_template('data/powericpenode.html', icpe = icpe)


@app.route('/data/heat')
def DataHeat():
    if request.method == 'GET':
        stats = NodeHeatStatModel.query.all()
        return render_template('data/heat.html', stats = stats)

@app.route('/data/heat/<mac>')
def DataHeatiCPE(mac):
    if request.method == 'GET':
        icpe = iCPEModel.query.filter_by(mac = mac).first()
        return render_template('data/heaticpe.html', icpe = icpe)

@app.route('/data/heat/<mac>/<nodeid>')
def DataHeatiCPENode(mac, nodeid):
    if request.method == 'GET':
        icpe = iCPEModel.query.filter_by(mac = mac).first()
        return render_template('data/heaticpenode.html', icpe = icpe)


