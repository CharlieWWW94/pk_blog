animatedText = document.querySelectorAll('.from-left');
console.log(animatedText);
const options = {

}

const observer = new IntersectionObserver(function (entries, observer) {
entries.forEach(entry => {
    if (entry.isIntersecting) {
    entry.target.classList.add('appear');
    };
    });
}, options);


animatedText.forEach(item => observer.observe(item));