function getPerros(numPerros, done) {
    fetch(`https://dog.ceo/api/breed/hound/images/random/${numPerros}`)
        .then(response => response.json())
        .then(data => {
            done(data);
        })
        .catch(error => {
            console.error('Error al obtener las imágenes de perros:', error);
        });
}

document.addEventListener("DOMContentLoaded", () => {
    const numPerros = 9;
    getPerros(numPerros, data => {
        if (data.status === "success") {
            const perros = data.message;
            
            perros.forEach(perroUrl => {
                const article = document.createRange().createContextualFragment(/*html*/`
                    <article>
                        <div class="image-container" style="max-height: 400px;">
                            <img src="${perroUrl}" alt="perro">
                        </div>
                        <h2>Perro</h2>
                        <span>Perro</span>
                    </article>
                `);

                const main = document.querySelector("main");
                main.append(article);
            });
        } else {
            console.error('Error al obtener las imágenes de perros');
        }
    });
});
