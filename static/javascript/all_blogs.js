
let htmlString = '';
let toFill = document.querySelector(".grid-item-5")
for ( let i = 0; i < newResults.length; i++) {
    htmlString += `<a class="link-wrapper" href="{% url '1_blog' id=${newResults[i][3]} %}">
                        <div class="blog">
                            <div class="blog-header">
                            <h2 class="blog-count">${newResults[i][0]}</h2>
                            <h3 class="blog-strap">${newResults[i][1]}</h3>
                            <h4 class="blog-strap">Author: ${newResults[i][2]}</h4>
                            <p class="blog-strap">${newResults[i][3]}...</p>
                            <h4 class="blog-strap">${newResults[i][4]}</h4>
                            
                            </div>
                        </div>
                    </a>`
};

toFill.innerHTML = htmlString;