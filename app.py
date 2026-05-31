from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Egreso, FormaPago
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

# vincula la instancia de la base de datos (db) con la aplicacion (app)
db.init_app(app)

# Crear tablas automáticamente
with app.app_context():
    db.create_all()
    # Inicializar datos de formas de pago si no existen
    if FormaPago.query.count() == 0:
        formas_pago_iniciales = [
            FormaPago(desformapago="Efectivo", estado=1),
            FormaPago(desformapago="Tarjeta Débito", estado=1),
            FormaPago(desformapago="Tarjeta Crédito", estado=1),
            FormaPago(desformapago="Transferencia", estado=1),
        ]
        db.session.add_all(formas_pago_iniciales)
        db.session.commit()

# rutas
@app.route("/")
def inicio():
    egresos = Egreso.query.order_by(Egreso.fecha.desc()).all()
    return render_template("index.html", egresos=egresos)




@app.route("/egresos/crear", methods=["GET", "POST"])
def crear_egreso():
    if request.method == "POST":
        detalle = request.form.get("detalle", "").strip()
        monto = request.form.get("monto", "").strip()
        fecha = request.form.get("fecha", "").strip()
        idformapago = request.form.get("idformapago", "").strip()
        
        # Validaciones
        if not detalle:
            flash("Detalle es obligatorio", "error")
            return redirect(url_for("crear_egreso"))
        
        if not monto:
            flash("Monto es obligatorio", "error")
            return redirect(url_for("crear_egreso"))
        
        if not fecha:
            flash("Fecha es obligatoria", "error")
            return redirect(url_for("crear_egreso"))
        
        if not idformapago:
            flash("Forma de pago es obligatoria", "error")
            return redirect(url_for("crear_egreso"))
        
        try:
            monto = float(monto)
            if monto <= 0:
                flash("El monto debe ser mayor a 0", "error")
                return redirect(url_for("crear_egreso"))
        except ValueError:
            flash("El monto debe ser un número válido", "error")
            return redirect(url_for("crear_egreso"))
        
        nuevo_egreso = Egreso(
            detalle=detalle,
            monto=monto,
            fecha=fecha,
            idformapago=idformapago,
        )
        db.session.add(nuevo_egreso)
        db.session.commit()
        flash(f'✅ Egreso "{detalle}" creado exitosamente', "success")
        return redirect(url_for("inicio"))
    formas_pago = FormaPago.query.all()
    return render_template("crear.html", formas_pago=formas_pago)


@app.route("/egresos/editar/<int:id>", methods=["GET", "POST"])
def editar_egreso(id):
    egreso = Egreso.query.get_or_404(id)
    if request.method == "POST":
        detalle = request.form.get("detalle", "").strip()
        monto = request.form.get("monto", "").strip()
        fecha = request.form.get("fecha", "").strip()
        idformapago = request.form.get("idformapago", "").strip()
        
        # Validaciones
        if not detalle:
            flash("Detalle es obligatorio", "error")
            return redirect(url_for("editar_egreso", id=id))
        
        if not monto:
            flash("Monto es obligatorio", "error")
            return redirect(url_for("editar_egreso", id=id))
        
        if not fecha:
            flash("Fecha es obligatoria", "error")
            return redirect(url_for("editar_egreso", id=id))
        
        if not idformapago:
            flash("Forma de pago es obligatoria", "error")
            return redirect(url_for("editar_egreso", id=id))
        
        try:
            monto = float(monto)
            if monto <= 0:
                flash("El monto debe ser mayor a 0", "error")
                return redirect(url_for("editar_egreso", id=id))
        except ValueError:
            flash("El monto debe ser un número válido", "error")
            return redirect(url_for("editar_egreso", id=id))
        
        egreso.detalle = detalle
        egreso.monto = monto
        egreso.fecha = fecha
        egreso.idformapago = idformapago

        db.session.commit()
        flash(f'✏️ Egreso "{egreso.detalle}" actualizado', "success")
        return redirect(url_for("inicio"))
    formas_pago = FormaPago.query.all()
    return render_template("editar.html", egreso=egreso, formas_pago=formas_pago)

@app.route("/egresos/eliminar/<int:id>")
def eliminar_egreso(id):
    egreso = Egreso.query.get_or_404(id)
    detalle = egreso.detalle

    db.session.delete(egreso)
    db.session.commit()
    flash(f'🗑️ Egreso "{detalle}" eliminado', "warning")
    return redirect(url_for("inicio"))

@app.route("/egresos/buscar")
def buscar_egreso():
    query = request.args.get("q", "")

    if query:
        egresos = (
            Egreso.query.filter(Egreso.detalle.contains(query))
            .order_by(Egreso.fecha.desc())
            .all()
        )
    else:
        egresos = []
    return render_template("buscar.html", egresos=egresos, query=query)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)