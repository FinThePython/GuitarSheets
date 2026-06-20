// This function gets the chord data from the get-chord-diagrams route
async function getChordDiagrams() {
    // Use 'try' in case of error 
    try {
        // Await for data to be fetched to avoid unexpected results 
        const response = await fetch('/get-chord-diagrams', {
            method: "GET"
        })
        // Error handling in case back end can't be pinged for the data 
        if (!response.ok) {
            throw new Error("Could not fetch data")
        }
        // Get the chord data and return it 
        const data = await response.json()
        return data
    }   catch (error) {
        console.error(error)
    }
}

// This function handles displaying the chord diagrams
async function displayChordDiagrams() {
    // Wait for the chord data to be fetched
    const chordsData = await getChordDiagrams()

    // Extract the chord data iteratively 
    var count = chordsData.length
    for (let i = 0; i < count; i++) {
        chordName = chordsData[i]["chordName"]
        startingFret = chordsData[i]["startingFret"]
        stringMarkers = chordsData[i]["stringMarkers"]
        frettedPositions = chordsData[i]["frettedPositions"]
        // Chord data is passed into the function that draws the chords
        drawChordDiagram(chordName, startingFret, stringMarkers, frettedPositions)
    }
}

// This function draws the chord diagrams to the document
function drawChordDiagram(chordName, startingFret, stringMarkers, frettedPositions) {
    // These constants will be used many times in this function
    const strings = 6
    const frets = 5

    // Get the container for all the chord diagrams to append to at the end
    const chordsContainer = document.getElementById("display-chords-container")
    
    // Create the container for each specific diagram
    const diagram = document.createElement("div")
    diagram.classList.add("chord-diagram")
    chordsContainer.appendChild(diagram)

    // Display the chord name
    const diagramChordName = document.createElement("div")
    diagramChordName.classList.add("chord-name")
    diagramChordName.style.fontWeight = "bold"
    diagramChordName.style.textDecoration ="underline"
    diagramChordName.textContent = `${chordName}`
    diagram.appendChild(diagramChordName)
    
    // Display the starting fret
    const diagramStartingFret = document.createElement("div")
    diagramStartingFret.classList.add("chord-name")
    diagramStartingFret.style.fontWeight = "bold"
    diagramStartingFret.textContent = `Starting Fret: ${startingFret}`
    diagram.appendChild(diagramStartingFret)

    // Display string markers
    const diagramStringMarkers = document.createElement("div")
    diagramStringMarkers.classList.add("string-markers")
    // Draw each marker 
    var percentLeft = 0
    // This loop creates each marker element
    for (let markerCount = 0; markerCount < strings; markerCount++) {
        let mark = document.createElement("p")
        mark.classList.add("string-mark")
        mark.style.cursor = "auto"
        mark.style.left = `${percentLeft}%`
        mark.textContent = stringMarkers[markerCount]
        percentLeft += 20
        diagramStringMarkers.appendChild(mark)
    }
    diagram.appendChild(diagramStringMarkers)

    // Display the fretboard
    const diagramFretBoard = document.createElement("div")
    diagramFretBoard.classList.add("fretboard")

    // Display notch/nut 
    const diagramNotch = document.createElement("div")
    diagramNotch.classList.add("notch")
    diagramFretBoard.append(diagramNotch)

    // Display the dots
    const diagramGrid = document.createElement("div")
    diagramGrid.classList.add("grid")
    console.log(frettedPositions)
    console.log(frettedPositions[0])
    // This loop to create each cell where dots go in
    for (let fretIndex = 1; fretIndex < frets; ++fretIndex){
        for (let stringIndex = 1; stringIndex < strings + 1; ++stringIndex){
            let dot = document.createElement("div")
            dot.classList.add("static-dot")
            // Remove point cursor effect
            dot.style.cursor = "auto"
            // If the position should have a visible dot, add the 'active' class
            if (Number(frettedPositions[stringIndex-1]) === fretIndex){
                dot.classList.add("active")
            }
            diagramGrid.appendChild(dot)
        }
    }
    diagramFretBoard.appendChild(diagramGrid)

    // Draw each string
    var percentLeft = 20
    // This loop creates each string and places it 20% more to the left each time
    for (let stringCount = 0; stringCount<(strings-2); stringCount++) {
        let string = document.createElement("div")
        string.classList.add("string")
        string.style.left = `${percentLeft}%`
        percentLeft += 20
        diagramFretBoard.appendChild(string)
    }
    // Draw each fret
    var percentTop = 25
    // This loop creates each fret and places it 20% more to the left each time
    for (let fretCount = 0; fretCount<(frets-2); fretCount++) {
        let fret = document.createElement("div")
        fret.classList.add("fret")
        fret.style.top = `${percentTop}%`
        percentTop += 25
        diagramFretBoard.appendChild(fret)
    }
    diagram.appendChild(diagramFretBoard)

    // Display the string numbers
    const diagramStringNumbers = document.createElement("div")
    diagramStringNumbers.classList.add("string-numbers")
    var percentLeft = 0
    // This loop creates a p element for each string number
    for (let stringCount = 0; stringCount < strings; stringCount++) {
        let numb = document.createElement("p")
        numb.classList.add("string-number")
        numb.style.left = `${percentLeft}%`
        numb.textContent = String(stringCount + 1)
        percentLeft += 20
        diagramStringNumbers.appendChild(numb)
    }
    diagram.appendChild(diagramStringNumbers)

    // Create a delete button 
    const diagramDeleteButton = document.createElement("button")
    diagramDeleteButton.classList.add("btn")
    diagramDeleteButton.classList.add("btn-danger")
    diagramDeleteButton.textContent = "Delete Chord"
    diagramDeleteButton.addEventListener("click", function(){
        deleteChordDiagram(chordName)
    })
    diagram.appendChild(diagramDeleteButton)
} 
displayChordDiagrams()

// This function will post the name of the chord that needs to be deleted to the backend
function deleteChordDiagram(chordName){
    // Send the data by post
    fetch('/delete-chord-diagram' , {
        method: 'POST',
        headers : {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(chordName)
    })
    
    .then(response => response.json())
    .then(data => {
        // refresh after the server has processed the request
        window.location.href = "/chord-diagrams";
    })
    .catch(err => console.error("Error:", err));
}



