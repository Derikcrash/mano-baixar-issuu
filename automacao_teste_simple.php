<?php

$pdf_url = "https://investidorinstitucional.com.br/wp-content/uploads/2026/08/institucional_389_completa-02.pdf";

$pdf = file_get_contents($pdf_url);

file_put_contents("edicao_389.pdf", $pdf);

echo "Baixado: edicao_389.pdf";

?>

#nao funciona