document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("memeForm");
  const btn  = form.querySelector(".generate-btn");
  const resultContainer = document.getElementById("resultContainer");
  const loader = resultContainer.querySelector(".loader");
  const imgEl  = document.getElementById("memeResult");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    // reset & show frame + spinner
    imgEl.src = "";
    resultContainer.classList.remove("hidden");
    loader.style.display = "block";

    btn.disabled = true;
    btn.classList.add("loading");

    try {
      const resp = await fetch("/generate", {
        method: "POST",
        body: new FormData(form)
      });
      if (!resp.ok) throw new Error(resp.statusText);
      const blob = await resp.blob();
      const url  = URL.createObjectURL(blob);

      // hide spinner, show image
      loader.style.display = "none";
      imgEl.src = url;
    } catch (err) {
      console.error(err);
      alert("Failed to generate meme");
      loader.style.display = "none";
    } finally {
      btn.disabled = false;
      btn.classList.remove("loading");
    }
  });
});
