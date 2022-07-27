function searchResults(toDisplay) {
    let toFill = document.querySelector(".grid-item-5")
    let htmlString = '';
    for ( let i = 0; i < toDisplay.length; i++) {
        
        
        htmlString += `<a class="link-wrapper" href="{% url '1_blog' id=${toDisplay[i][3]} %}">
                            <div class="blog">
                                <div class="blog-header">
                                <h2 class="blog-count">${toDisplay[i][0]}</h2>
                                <h3 class="blog-strap">${toDisplay[i][1]}</h3>
                                <h4 class="blog-strap">Author: ${toDisplay[i][2]}</h4>
                                <p class="blog-strap">${toDisplay[i][3]}...</p>
                                <h4 class="blog-strap blog-date">${toDisplay[i][4]}</h4>
                                
                                </div>
                            </div>
                        </a>`
    };

    toFill.innerHTML = htmlString;

}

const oldFilter = document.querySelector("#oldest");
const newFilter = document.querySelector("#newest");

newFilter.addEventListener("click", () => {
    newResults = newResults.reverse();
    console.log(newResults);
    searchResults(newResults);
})

oldFilter.addEventListener("click", () => {
    newResults = newResults.reverse();
    console.log(newResults);
    searchResults(newResults);
});



searchResults(newResults);