document.addEventListener("DOMContentLoaded", function () {
  createGraficoDiscapacidades();
  createGraficoCobros();
  createGraficoPuestos();
});

function createGraficoDiscapacidades() {
  const labels = JSON.parse(
    document.getElementById("data-grafico-discapacidades").dataset.labels
  );
  const cants = JSON.parse(
    document.getElementById("data-grafico-discapacidades").dataset.cants
  );

  const data = {
    labels: labels,
    datasets: [
      {
        backgroundColor: [
          "#66b4d1",
          "#458cb1",
          "#29658f",
          "#11406c",
          "#001e49",
        ],
        hoverOffset: 4,
        data: cants,
      },
    ],
  };

  const legends = {
    position: "right",
  };

  const config = {
    type: "pie",
    data: data,
    options: {
      maintainAspectRatio: false,
      cutout: 0,
      plugins: { legend: legends },
    },
  };

  new Chart(document.getElementById("canvas-grafico-discapacidades"), config);
}

function createGraficoCobros() {
  const montos_por_mes = JSON.parse(
    document.getElementById("data-grafico-cobros").dataset.data
  );

  const labels = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
  ];
  const data = {
    labels: labels,
    datasets: [
      {
        label: "Monto total por mes (ARS)",
        data: montos_por_mes,
        fill: false,
        borderColor: "#E1B44B",
        tension: 0.1,
      },
    ],
  };

  const config = {
    type: "line",
    data: data,
  };

  new Chart(document.getElementById("canvas-grafico-cobros"), config);
}

function createGraficoPuestos() {
  const cant_por_puesto = JSON.parse(
    document.getElementById("data-grafico-puestos").dataset.data
  );

  const cantidades = cant_por_puesto.map((item) => item.cant);

  const labels = [
    "Administrativo/a",
    "Terapeuta",
    "Conductor",
    "Auxiliar de pista",
    "Herrero",
    "Veterinario",
    "Entrenador de caballos",
    "Domador",
    "Profesor de equitación",
    "Docente de capacitación",
    "Auxiliar de mantenimiento",
    "Otro",
  ];
  const data = {
    labels: labels,
    datasets: [
      {
        label: "Cantidad de empleados",
        data: cantidades,
        fill: false,
        backgroundColor: [
          "rgba(102, 180, 209, 0.2)",
          "rgba(123, 180, 197, 0.2)",
          "rgba(139, 180, 186, 0.2)",
          "rgba(153, 180, 174, 0.2)",
          "rgba(165, 180, 163, 0.2)",
          "rgba(176, 180, 151, 0.2)",
          "rgba(186, 180, 139, 0.2)",
          "rgba(195, 180, 127, 0.2)",
          "rgba(203, 180, 115, 0.2)",
          "rgba(211, 180, 102, 0.2)",
          "rgba(218, 180, 89, 0.2)",
          "rgba(225, 180, 75, 0.2)",
        ],
        borderColor: [
          "rgb(102, 180, 209)",
          "rgb(123, 180, 197)",
          "rgb(139, 180, 186)",
          "rgb(153, 180, 174)",
          "rgb(165, 180, 163)",
          "rgb(176, 180, 151)",
          "rgb(186, 180, 139)",
          "rgb(195, 180, 127)",
          "rgb(203, 180, 115)",
          "rgb(211, 180, 102)",
          "rgb(218, 180, 89)",
          "rgb(225, 180, 75)",
        ],
        borderWidth: 1,
        minBarLength: 5,
      },
    ],
  };

  const config = {
    type: "bar",
    data: data,
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  };

  new Chart(document.getElementById("canvas-grafico-puestos"), config);
}
