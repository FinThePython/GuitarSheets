// Global Variables
const strings = 6
const frets = 5

// O = Open X = Muted ""= Fretted
var stringMarkers = ["O","O","O","O","O","O"]

// This function draws the string markers
function drawStringMarkers () {
    // Get the element we want to draw the marks in
    const stringMarkers = document.getElementById("string-markers")

    // Draw each marker 
    var percentLeft = 0
    // This loop creates each marker element
    for (let markerCount = 0; markerCount < strings; markerCount++) {
        let mark = document.createElement("p")
        mark.dataset.string = markerCount
        // Check if the user wishes to change it
        mark.addEventListener("click", function () {
            toggleMarkers(mark)
        })
        mark.classList.add("string-mark")
        mark.style.left = `${percentLeft}%`
        mark.textContent = "O"
        percentLeft += 20
        stringMarkers.appendChild(mark)
    }

}

// This function handles the click on string markers
function toggleMarkers (mark){
    currentMark = mark.textContent
    // Toggle between open, muted and no mark
    if (currentMark === "O") {
        currentMark = "X"
    } 
    else if (currentMark === "X"){
        currentMark = ""
    }
    else if (currentMark === "") {
        currentMark = "O"
    }
    // Make the changes in the document and data structure 
    stringMarkers[mark.dataset.string] = currentMark
    console.log(stringMarkers)
    mark.textContent = currentMark
}

// number = fret, index = string
var frettedPositions = [0,0,0,0,0,0]

// This function draws out the fretboard 
function drawFretBoard () {
    // Get the fretboard from the document
    const fretBoard = document.getElementById("fretboard")

    // Draw each string
    var percentLeft = 20
    // This loop creates each string and places it 20% more to the left each time
    for (let stringCount = 0; stringCount<(strings-2); stringCount++) {
        let string = document.createElement("div")
        string.classList.add("string")
        string.style.left = `${percentLeft}%`
        percentLeft += 20
        fretBoard.appendChild(string)
    }

    // Draw each fret
    var percentTop = 25
    // This loop creates each fret and places it 20% more to the left each time
    for (let fretCount = 0; fretCount<(frets-2); fretCount++) {
        let fret = document.createElement("div")
        fret.classList.add("fret")
        fret.style.top = `${percentTop}%`
        percentTop += 25
        fretBoard.appendChild(fret)
    }
}

// This function creates a grid of clickable cells to edit the fretboard
function createGrid () {
    // Get the gird element from the document
    const grid = document.getElementById("grid")

    // This loop creates each clickable cell
    for (let fretIndex = 1; fretIndex < frets; ++fretIndex){
        for (let stringIndex = 1; stringIndex < strings + 1; ++stringIndex){
            // Add hidden dots that are made visible on click
            let dot = document.createElement("div")
            dot.classList.add("dot")
            dot.dataset.fret = fretIndex
            dot.dataset.string = stringIndex
            dot.addEventListener("click", function() {
                drawDots(dot)
            })
            grid.appendChild(dot)
        }
    }
}

// This function draws dots
function drawDots(dot){
    // Get all dots on the string selected
    frettedString = dot.dataset.string
    frettedFret = dot.dataset.fret

    // Removes dot if already placed in that spot
    if (dot.classList.contains("active")){
        dot.classList.remove("active")
        frettedPositions[frettedString-1] = 0
        console.log(frettedPositions)
        return; // End the function
    }

    else {
        // Clear all dots on the string 
        dotsOnString = document.querySelectorAll(`.dot[data-string="${frettedString}"]`)
        dotsOnString.forEach(dot => { dot.classList.remove("active")})
        // Draw new dot
        frettedPositions[frettedString-1] = frettedFret
        console.log(frettedPositions)
        dot.classList.add("active")
    }   
}

// This function draws out the string numbers
function drawStringNumbers () {
    // Get the element we want to draw the marks in
    const stringNumbers = document.getElementById("string-numbers")

    var percentLeft = 0
    // This loop creates a p element for each string
    for (let stringCount = 0; stringCount < strings; stringCount++) {
        console.log(stringCount)
        let numb = document.createElement("p")
        numb.classList.add("string-number")
        numb.style.left = `${percentLeft}%`
        numb.textContent = String(stringCount + 1)
        percentLeft += 20
        stringNumbers.appendChild(numb)
    }
}

// Run all the functions to draw the diagram
drawStringMarkers()
drawFretBoard()
createGrid()
drawStringNumbers()

// This function handles saving the chord diagram on button press
function saveChordDiagram () {
    // Take the data we want to send and put it in an object
    const chordData = {
        stringMarkers: stringMarkers,
        frettedPositions: frettedPositions,
        chordName: document.getElementById("chordName").value,
        startingFret: document.getElementById("startingFret").value,
    } 
    // Send the data by post
    fetch('/save-chord-diagram' , {
        method: 'POST',
        headers : {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(chordData)
    })
    
    .then(response => response.json())
    .then(data => {
        // Only redirect AFTER the server has processed the request
        window.location.href = "/create-chord-diagram";
    })
    .catch(err => console.error("Error:", err));
}
