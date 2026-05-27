let scanner = null;

const API_BASE = "http://127.0.0.1:8000";

const codeInput =
  document.getElementById("codeInput");

codeInput.addEventListener("keydown",(e)=>{

  if(e.key === "Enter"){
    searchItem();
  }

});

/* QR SCANNER */

function startScanner(){

  const reader =
    document.getElementById("reader");

  reader.style.display = "block";

  scanner = new Html5Qrcode("reader");

  scanner.start(

    {
      facingMode:"environment"
    },

    {
      fps:10,
      qrbox:250
    },

    onScanSuccess

  ).catch(err=>{

    console.error(err);

    setStatus(
      "Camera access failed",
      true
    );

  });

}

async function onScanSuccess(decodedText){

  try{

    if(scanner){

      await scanner.stop();

      document.getElementById("reader")
      .style.display = "none";

    }

    document.getElementById("codeInput")
    .value = decodedText;

    searchItem();

    if(navigator.vibrate){
      navigator.vibrate(200);
    }

  }catch(err){

    console.error(err);

  }

}

/* SEARCH */

async function searchItem(){

  const code =
    codeInput.value.trim();

  if(!code){
    return;
  }

  try{

    setStatus("Searching...");

    const response = await fetch(
      `${API_BASE}/search/${code}`
    );

    const item = await response.json();

    if(item.error){

      document.getElementById("resultCard")
      .style.display = "none";

      document.getElementById("emptyState")
      .style.display = "flex";

      setStatus(
        "Item not found",
        true
      );

      return;
    }

    renderItem(item);

    setStatus(
      `✓ Found ${item.unique_code}`,
      false,
      true
    );

  }catch(err){

    console.error(err);

    setStatus(
      "Server connection failed",
      true
    );

  }

}

/* RENDER */

function renderItem(item){

  document.getElementById("emptyState")
  .style.display = "none";

  document.getElementById("resultCard")
  .style.display = "block";

  document.getElementById("title")
  .innerText = item.unique_code;

  document.getElementById("subtitle")
  .innerText = item.design;

  document.getElementById("collection")
  .innerText = item.collection || "-";

  document.getElementById("styleCode")
  .innerText = item.style_code || "-";

  document.getElementById("goldType")
  .innerText = item.kt_col || "-";

  document.getElementById("grossWt")
  .innerText = item.gross_wt || "-";

  document.getElementById("netWt")
  .innerText = item.net_wt || "-";

  document.getElementById("itemSize")
  .innerText = item.item_size || "-";

  document.getElementById("qty")
  .innerText = item.qty || "-";

  document.getElementById("salePrice")
  .innerText =
    `$${parseFloat(item.sale_price || 0).toFixed(2)}`;

  document.getElementById("productImage")
  .src = `${API_BASE}${item.image}`;

}

/* STATUS */

function setStatus(
  message,
  isError=false,
  isSuccess=false
){

  const status =
    document.getElementById("status");

  status.innerText = message;

  status.className = "status";

  if(isError){
    status.classList.add("notFound");
  }

  if(isSuccess){
    status.classList.add("success");
  }

}
