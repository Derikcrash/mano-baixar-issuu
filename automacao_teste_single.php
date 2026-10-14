<?php

$url_pagina = "https://investidorinstitucional.com.br/edicoes-anteriores-em-pdf/";

$html = file_get_contents($url_pagina);

$padrao = "/FB3D_CLIENT_DATA\.push\('([^']+)'\)/";

preg_match_all($padrao, $html, $dados);

$edicao_desejada = 389;

foreach ($dados[1] as $codigo) {

    $decodificado = base64_decode($codigo);

    $json_data = json_decode($decodificado, true);

    $post = array_values($json_data["posts"])[0];

    $titulo = $post["title"];

    preg_match('/\d+/', $titulo, $numero);

    $numero_edicao = $numero[0];

    if ($numero_edicao == $edicao_desejada) {

        $pdf_url = $post["data"]["guid"];

        $pdf = file_get_contents($pdf_url);

        file_put_contents("edicao_{$numero_edicao}.pdf", $pdf);

        echo "Baixado: edicao_{$numero_edicao}.pdf<br>";

        break;
    }
}

?>