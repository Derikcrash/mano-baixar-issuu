<?php

$url_pagina = "https://investidorinstitucional.com.br/edicoes-anteriores-em-pdf/";

$html = file_get_contents($url_pagina);

$padrao = "/FB3D_CLIENT_DATA\.push\('([^']+)'\)/";

preg_match_all($padrao, $html, $dados);

$codigo = $dados[1][0];

$decodificado = base64_decode($codigo);

$json_data = json_decode($decodificado, true);

$post = array_values($json_data["posts"])[0];

$titulo = $post["title"];

$pdf_url = $post["data"]["guid"];

$pdf = file_get_contents($pdf_url);

file_put_contents("{$titulo}.pdf", $pdf);

echo "Baixado: {$titulo}.pdf";

?>
