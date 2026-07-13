from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Egreso, FormaPago
from config import Config
from datetime import datetime
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
        detalle = request.form.get("detalle")
        monto = request.form.get("monto")
        fecha_str = request.form.get("fecha")
        idformapago = request.form.get("idformapago")

        if not detalle or not monto or not fecha_str or not idformapago:
            flash("Todos los campos marcados con asterisco (*) son obligatorios.", "danger")
            formas_pago = FormaPago.query.filter_by(estado=1).all()
            return render_template("crear.html", formas_pago=formas_pago)

        try:
            # Convertimos la fecha de string HTML 'YYYY-MM-DD' a objeto date de Python
            fecha_objeto = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            
            nuevo_egreso = Egreso(
                detalle=detalle,
                monto=float(monto),
                fecha=fecha_objeto,  # Usamos el objeto date convertido
                idformapago=int(idformapago)
            )
            
            db.session.add(nuevo_egreso)
            db.session.commit()
            flash("Egreso registrado con éxito.", "success")
            return redirect(url_for("inicio"))

        except ValueError as e:
            db.session.rollback()
            flash(f"Error en el formato de datos: {str(e)}", "danger")
        except Exception as e:
            db.session.rollback()
            flash(f"Ocurrió un error inesperado: {str(e)}", "danger")

    formas_pago = FormaPago.query.filter_by(estado=1).all()
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
