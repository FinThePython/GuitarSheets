// This function gets the chord sheet data from the get-chord-sheets route
async function getChordSheets() {
    // Use 'try' in case of error 
    try {
        // Await for data to be fetched to avoid unexpected results 
        const response = await fetch('/get-chord-sheets', {
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

// This function displays the user's chord sheets as links to view them fully
async function displayChordSheets() {
    //Call the getChordSheets function 
    songs = await getChordSheets()
    
    // Extract the data iteratively to display links to each chord sheet
    var count = songs.length 
    for (let i=0; i < count; i++) {
        songName = songs[i]["songName"]
        artist = songs[i]["artist"]
        difficulty = songs[i]["difficulty"]
        id = songs[i]["id"]
        // call function to display links
        displayLinks(songName, artist, difficulty, id)
    }
}

// Global Variables used for filtering/searching
const searchInput = document.getElementById("search")
const linksContainer = document.getElementById("links-container")

let currentLinks = []

// This function will add the link elements to the page for the user to find their chord sheets
function displayLinks(songName, artist, difficulty, id) {
    // Make the wrapper for each link
    const wrapper = document.createElement("div")
    wrapper.classList.add("link")
    linksContainer.appendChild(wrapper)

    // Create link to chord sheet
    const songLink =  document.createElement("a")
    songLink.href = `/view-chord-sheet/${id}`
    songLink.textContent = `${songName} - ${artist} - ${difficulty}`
    wrapper.appendChild(songLink)

    // Create link to edit chord sheet
    const editLink =  document.createElement("a")
    editLink.href = `/edit-chord-sheet/${id}`
    editLink.classList.add("edit")
    editLink.textContent = "[Edit]"
    wrapper.appendChild(editLink)

    // Create link to delete chord sheet
    const deleteLink =  document.createElement("a")
    deleteLink.href = `/delete-chord-sheet/${id}`
    deleteLink.classList.add("delete")
    deleteLink.textContent = "[Delete]"
    wrapper.appendChild(deleteLink)

    // Store data for search purposes 
    currentLinks.push({
        name: songName.toLowerCase(),
        artist: artist.toLowerCase(),
        difficulty: difficulty.toLowerCase(),
        element: wrapper
    })
}

function searchFunctionality() {
    // Search functionality
    searchInput.addEventListener("input", link => {
        // Make everything lowercase to ensure searching works without 
        const value = link.target.value.toLowerCase()
    
        // For each link check if the inputted data matches 
        currentLinks.forEach(song => {
            const isVisible =
                song.name.includes(value) ||
                song.artist.includes(value) ||
                song.difficulty.includes(value)
    
            // Hide links that don't match
            song.element.classList.toggle("hide", !isVisible)
        })
    })
    
}

searchFunctionality()
displayChordSheets()