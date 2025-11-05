// 1. Inicializar red neuronal
var network = new brain.NeuralNetwork();

// 2. Datos de entrenamiento (los 30 registros que generamos)
var trainingData = [
  {input: {SepalLengthCm: 4.3, SepalWidthCm: 3.0, PetalLengthCm: 1.1, PetalWidthCm: 0.1}, output: {setosa: 1, versicolor: 0, virginica: 0}},
  {input: {SepalLengthCm: 5.1, SepalWidthCm: 3.4, PetalLengthCm: 1.5, PetalWidthCm: 0.2}, output: {setosa: 1, versicolor: 0, virginica: 0}},
  {input: {SepalLengthCm: 4.8, SepalWidthCm: 3.1, PetalLengthCm: 1.6, PetalWidthCm: 0.2}, output: {setosa: 1, versicolor: 0, virginica: 0}},
  {input: {SepalLengthCm: 4.8, SepalWidthCm: 3.0, PetalLengthCm: 1.4, PetalWidthCm: 0.3}, output: {setosa: 1, versicolor: 0, virginica: 0}},
  {input: {SepalLengthCm: 5.1, SepalWidthCm: 3.5, PetalLengthCm: 1.4, PetalWidthCm: 0.3}, output: {setosa: 1, versicolor: 0, virginica: 0}},
  {input: {SepalLengthCm: 5.3, SepalWidthCm: 3.7, PetalLengthCm: 1.5, PetalWidthCm: 0.2}, output: {setosa: 1, versicolor: 0, virginica: 0}},
  {input: {SepalLengthCm: 5.0, SepalWidthCm: 3.4, PetalLengthCm: 1.6, PetalWidthCm: 0.4}, output: {setosa: 1, versicolor: 0, virginica: 0}},
  {input: {SepalLengthCm: 5.0, SepalWidthCm: 3.0, PetalLengthCm: 1.6, PetalWidthCm: 0.2}, output: {setosa: 1, versicolor: 0, virginica: 0}},
  {input: {SepalLengthCm: 5.2, SepalWidthCm: 4.1, PetalLengthCm: 1.5, PetalWidthCm: 0.1}, output: {setosa: 1, versicolor: 0, virginica: 0}},
  {input: {SepalLengthCm: 5.1, SepalWidthCm: 3.8, PetalLengthCm: 1.5, PetalWidthCm: 0.3}, output: {setosa: 1, versicolor: 0, virginica: 0}},
  {input: {SepalLengthCm: 5.7, SepalWidthCm: 2.6, PetalLengthCm: 3.5, PetalWidthCm: 1.0}, output: {setosa: 0, versicolor: 1, virginica: 0}},
  {input: {SepalLengthCm: 5.6, SepalWidthCm: 3.0, PetalLengthCm: 4.1, PetalWidthCm: 1.3}, output: {setosa: 0, versicolor: 1, virginica: 0}},
  {input: {SepalLengthCm: 6.9, SepalWidthCm: 3.1, PetalLengthCm: 4.9, PetalWidthCm: 1.5}, output: {setosa: 0, versicolor: 1, virginica: 0}},
  {input: {SepalLengthCm: 5.7, SepalWidthCm: 2.9, PetalLengthCm: 4.2, PetalWidthCm: 1.3}, output: {setosa: 0, versicolor: 1, virginica: 0}},
  {input: {SepalLengthCm: 5.7, SepalWidthCm: 3.0, PetalLengthCm: 4.2, PetalWidthCm: 1.2}, output: {setosa: 0, versicolor: 1, virginica: 0}},
  {input: {SepalLengthCm: 5.5, SepalWidthCm: 2.5, PetalLengthCm: 4.0, PetalWidthCm: 1.3}, output: {setosa: 0, versicolor: 1, virginica: 0}},
  {input: {SepalLengthCm: 6.3, SepalWidthCm: 2.5, PetalLengthCm: 4.9, PetalWidthCm: 1.5}, output: {setosa: 0, versicolor: 1, virginica: 0}},
  {input: {SepalLengthCm: 5.6, SepalWidthCm: 2.7, PetalLengthCm: 4.2, PetalWidthCm: 1.3}, output: {setosa: 0, versicolor: 1, virginica: 0}},
  {input: {SepalLengthCm: 5.0, SepalWidthCm: 2.0, PetalLengthCm: 3.5, PetalWidthCm: 1.0}, output: {setosa: 0, versicolor: 1, virginica: 0}},
  {input: {SepalLengthCm: 7.0, SepalWidthCm: 3.2, PetalLengthCm: 4.7, PetalWidthCm: 1.4}, output: {setosa: 0, versicolor: 1, virginica: 0}},
  {input: {SepalLengthCm: 5.8, SepalWidthCm: 2.7, PetalLengthCm: 5.1, PetalWidthCm: 1.9}, output: {setosa: 0, versicolor: 0, virginica: 1}},
  {input: {SepalLengthCm: 5.9, SepalWidthCm: 3.0, PetalLengthCm: 5.1, PetalWidthCm: 1.8}, output: {setosa: 0, versicolor: 0, virginica: 1}},
  {input: {SepalLengthCm: 7.6, SepalWidthCm: 3.0, PetalLengthCm: 6.6, PetalWidthCm: 2.1}, output: {setosa: 0, versicolor: 0, virginica: 1}},
  {input: {SepalLengthCm: 6.8, SepalWidthCm: 3.2, PetalLengthCm: 5.9, PetalWidthCm: 2.3}, output: {setosa: 0, versicolor: 0, virginica: 1}},
  {input: {SepalLengthCm: 7.2, SepalWidthCm: 3.0, PetalLengthCm: 5.8, PetalWidthCm: 1.6}, output: {setosa: 0, versicolor: 0, virginica: 1}},
  {input: {SepalLengthCm: 6.4, SepalWidthCm: 2.8, PetalLengthCm: 5.6, PetalWidthCm: 2.1}, output: {setosa: 0, versicolor: 0, virginica: 1}},
  {input: {SepalLengthCm: 7.7, SepalWidthCm: 3.8, PetalLengthCm: 6.7, PetalWidthCm: 2.2}, output: {setosa: 0, versicolor: 0, virginica: 1}},
  {input: {SepalLengthCm: 6.3, SepalWidthCm: 2.9, PetalLengthCm: 5.6, PetalWidthCm: 1.8}, output: {setosa: 0, versicolor: 0, virginica: 1}},
  {input: {SepalLengthCm: 7.7, SepalWidthCm: 2.6, PetalLengthCm: 6.9, PetalWidthCm: 2.3}, output: {setosa: 0, versicolor: 0, virginica: 1}},
  {input: {SepalLengthCm: 6.4, SepalWidthCm: 3.2, PetalLengthCm: 5.3, PetalWidthCm: 2.3}, output: {setosa: 0, versicolor: 0, virginica: 1}}
];

// 3. Entrenar la red
// (Esto puede tardar unos segundos)
console.log("Entrenando red...");
network.train(trainingData, {
    iterations: 2000,
    log: true,
    logPeriod: 100,
    errorThresh: 0.005
});
console.log("Entrenamiento completado.");


/**
 * Función para predecir la especie de Iris basada en la entrada del formulario.
 * Esta reemplaza tu antigua función `update(color)`.
 */
function predecirEspecie() {
    // 1. Obtener los valores de los campos del formulario
    // Usamos parseFloat para convertir el texto del input en un número decimal
    var sepalLength = parseFloat(document.getElementById("SepalLengthCm").value);
    var sepalWidth = parseFloat(document.getElementById("SepalWidthCm").value);
    var petalLength = parseFloat(document.getElementById("PetalLengthCm").value);
    var petalWidth = parseFloat(document.getElementById("PetalWidthCm").value);

    // 2. Crear el objeto de entrada para la red
    var entrada = {
        SepalLengthCm: sepalLength,
        SepalWidthCm: sepalWidth,
        PetalLengthCm: petalLength,
        PetalWidthCm: petalWidth
    };

    // 3. Ejecutar la red con la entrada
    var resultado = network.run(entrada);
    
    // Imprimir el resultado crudo en la consola (ej: {setosa: 0.8, ...})
    console.log("Probabilidades:", resultado);

    // 4. Encontrar la especie con la probabilidad más alta
    var especieGanadora = "";
    var probMaxima = -1; // Empezamos con -1 para que cualquier probabilidad sea mayor

    // Iteramos sobre las claves del objeto resultado (setosa, versicolor, virginica)
    for (var especie in resultado) {
        if (resultado[especie] > probMaxima) {
            probMaxima = resultado[especie];
            especieGanadora = especie;
        }
    }

    // 5. Mostrar el resultado en la página
    var divResultado = document.getElementById("resultadoEspecie");
    divResultado.innerHTML = "Especie predicha: <strong>" + especieGanadora + "</strong> (Confianza: " + (probMaxima * 100).toFixed(2) + "%)";
}