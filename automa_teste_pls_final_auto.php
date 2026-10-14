<?php

$url_pagina = "https://investidorinstitucional.com.br/edicoes-anteriores-em-pdf/";

$html = file_get_contents($url_pagina);

$padrao = "/FB3D_CLIENT_DATA\.push\('([^']+)'\)/";

preg_match_all($padrao, $html, $dados);

foreach ($dados[1] as $codigo) {

    $decodificado = base64_decode($codigo);

    $json_data = json_decode($decodificado, true);

    foreach ($json_data["posts"] as $post) {

        $titulo = $post["title"];

        $pdf_url = $post["data"]["guid"];

        $nome_arquivo = "{$titulo}.pdf";

        if (file_exists($nome_arquivo)) {
            echo "Já existe: {$nome_arquivo}<br>";
            continue;
        }

        $pdf = file_get_contents($pdf_url);

        if ($pdf === false) {
            echo "Erro ao baixar: {$titulo}<br>";
            continue;
        }

        file_put_contents($nome_arquivo, $pdf);

        echo "Baixado: {$nome_arquivo}<br>";
    }
}

?>