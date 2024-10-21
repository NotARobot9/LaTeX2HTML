var refcontent = "Cualquier cosa";
var refnumactual;

function getref(laref) {
  switch (laref) {
    case 1:
      reflabel = "*";
      refcontent = "Recuerda que $v\\in V$ es un <em class='emph'>valor propio</em> (llamado también <em class='emph'>autovalor</em> o <em class='emph'>eigenvalor)</em> de la función lineal $L\\colon V\\rightarrow V$ si $v\\neq 0$ y $Lv=\\lambda v$ para algún $\\lambda \\in \\mathbb{R}$.";
      break;
    case 2:
      reflabel = "*";
      refcontent = 'Consulta,por ejemplo, el applet de M. Levoy, A. Adams, K. Dektar y N. Willett, <em class="emph">Spacial Convolution</em>, applet para el curso Digital Photography (Spring 2011), Stanford University. http://graphics.stanford.edu/courses/cs178/applets/convolution.html"';
      break;
    case 3:
      reflabel = "*";
      refcontent = 'De hecho, $\\Phi $ es también suprayectiva, lo que permite identificar a $\\mathcal{L}(L^{p}(\\Omega ),\\mathbb{R})$ con $L^{p/(p-1)}(\\Omega )$. A este resultado se le conoce como el <em class="emph">teorema de representación de Riesz</em>. Consulta, por ejemplo, {Bre}, Teorema IV.11.';
      break;      
    default:
      reflabel = "nada";
      refcontent = "$v\\in V$";
  }
}

function setVisibility(id, refnum) {
  if (document.getElementById(id).style.visibility == 'hidden') {
    getref(refnum);
    document.getElementById(id).innerHTML = "<div class='biblabel'>" +
      reflabel + "</div>" + "<div class='bibentry'>" +
      refcontent + "</div>";
    document.getElementById(id).style.visibility = 'visible';
    document.getElementById(id).style.display = 'inline';
      MathJax.Hub.Typeset();
    refnumactual = refnum;
  } else {
    if (refnumactual == refnum) {
      document.getElementById(id).style.visibility = 'hidden';
    } else {
      getref(refnum);
      document.getElementById(id).innerHTML = "<div class='biblabel'>" +
        reflabel + "</div>" + "<div class='bibentry'>" +
        refcontent + "</div>";
      document.getElementById(id).style.visibility = 'visible';
      document.getElementById(id).style.display = 'inline';
      MathJax.Hub.Typeset();

      refnumactual = refnum;
    }
  }
}

/*
'De hecho, $\\Phi $ es también suprayectiva, lo que permite identificar a $\\mathcal{L}(L^{p}(\\Omega ),\\mathbb{R})$ con $L^{p/(p-1)}(\\Omega )$. A este resultado se le conoce como el <em class="emph">teorema de representación de Riesz</em>. Consulta, por ejemplo,~\cite{Bre}, Teorema IV.11.';
      refcontent = 'Consulta,por ejemplo, el applet de M. Levoy, A. Adams, K. Dektar y N. Willett, <em class="emph">Spacial Convolution</em>, applet para el curso Digital Photography (Spring 2011), Stanford University. http://graphics.stanford.edu/courses/cs178/applets/convolution.html"';
*/