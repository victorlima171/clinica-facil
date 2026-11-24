
from flask import Flask, render_template, request, redirect, jsonify
from database import conectar, criar_banco

app = Flask(__name__)

criar_banco()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/pacientes")
def pacientes():
    conn = conectar()
    lista = conn.execute(
        "SELECT * FROM pacientes ORDER BY nome"
    ).fetchall()
    conn.close()

    busca = request.args.get("busca", "")

    if busca:
        resultado = []

        for paciente in lista:
            if busca.lower() in paciente["nome"].lower():
                resultado.append(paciente)

        lista = resultado

    return render_template("pacientes.html", pacientes=lista)


@app.route("/pacientes/cadastrar", methods=["GET", "POST"])
def cadastrar_paciente():
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        nascimento = request.form["data_nascimento"]

        conn = conectar()
        conn.execute(
            """INSERT INTO pacientes
            (nome, telefone, email, data_nascimento)
            VALUES (?, ?, ?, ?)""",
            (nome, telefone, email, nascimento)
        )
        conn.commit()
        conn.close()

        return redirect("/pacientes")

    return render_template("form_paciente.html", paciente=None)


@app.route("/pacientes/editar/<int:id>", methods=["GET", "POST"])
def editar_paciente(id):
    conn = conectar()

    if request.method == "POST":
        conn.execute(
            """UPDATE pacientes
            SET nome=?, telefone=?, email=?, data_nascimento=?
            WHERE id=?""",
            (
                request.form["nome"],
                request.form["telefone"],
                request.form["email"],
                request.form["data_nascimento"],
                id
            )
        )
        conn.commit()
        conn.close()

        return redirect("/pacientes")

    paciente = conn.execute(
        "SELECT * FROM pacientes WHERE id=?", (id,)
    ).fetchone()

    conn.close()

    if paciente is None:
        return "Paciente não encontrado", 404

    return render_template("form_paciente.html", paciente=paciente)


@app.route("/pacientes/excluir/<int:id>", methods=["POST"])
def excluir_paciente(id):
    conn = conectar()
    conn.execute("DELETE FROM pacientes WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/pacientes")


@app.route("/api/pacientes")
def api_pacientes():
    conn = conectar()
    lista = conn.execute(
        "SELECT * FROM pacientes ORDER BY nome"
    ).fetchall()
    conn.close()

    return jsonify([dict(paciente) for paciente in lista])



@app.route("/consultas")
def consultas():
    conn = conectar()

    lista = conn.execute("""
        SELECT consultas.*, pacientes.nome AS paciente
        FROM consultas
        JOIN pacientes ON consultas.paciente_id = pacientes.id
        ORDER BY consultas.data, consultas.horario
    """).fetchall()

    conn.close()

    return render_template("consultas.html", consultas=lista)


@app.route("/consultas/cadastrar", methods=["GET", "POST"])
def cadastrar_consulta():
    conn = conectar()

    if request.method == "POST":
        conn.execute("""
            INSERT INTO consultas
            (paciente_id, data, horario, especialidade, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            request.form["paciente_id"],
            request.form["data"],
            request.form["horario"],
            request.form["especialidade"],
            request.form["status"]
        ))

        conn.commit()
        conn.close()

        return redirect("/consultas")

    pacientes = conn.execute(
        "SELECT * FROM pacientes ORDER BY nome"
    ).fetchall()

    conn.close()

    return render_template(
        "form_consulta.html",
        pacientes=pacientes,
        consulta=None
    )


@app.route("/consultas/editar/<int:id>", methods=["GET", "POST"])
def editar_consulta(id):
    conn = conectar()

    if request.method == "POST":
        conn.execute("""
            UPDATE consultas
            SET paciente_id=?, data=?, horario=?,
                especialidade=?, status=?
            WHERE id=?
        """, (
            request.form["paciente_id"],
            request.form["data"],
            request.form["horario"],
            request.form["especialidade"],
            request.form["status"],
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/consultas")

    consulta = conn.execute(
        "SELECT * FROM consultas WHERE id=?", (id,)
    ).fetchone()

    pacientes = conn.execute(
        "SELECT * FROM pacientes ORDER BY nome"
    ).fetchall()

    conn.close()

    if consulta is None:
        return "Consulta não encontrada", 404

    return render_template(
        "form_consulta.html",
        consulta=consulta,
        pacientes=pacientes
    )


@app.route("/consultas/excluir/<int:id>", methods=["POST"])
def excluir_consulta(id):
    conn = conectar()
    conn.execute("DELETE FROM consultas WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/consultas")


if __name__ == "__main__":
    app.run()
