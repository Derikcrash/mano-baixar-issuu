<?php 
#Entra na URL e trás a resposta da requisição (conteúdo do site)
$resposta = file_get_contents('https://agrimidia.com.br/revistas/'); 

#padrao regex para captura de URL's e armazenamento em variável
$padrao_html = "/(https://agrimidia.com.br/revista/(?:ai|si)-edicao-\d+)/";
preg_match($padrao_html, $resposta, $resposta_match);

$resposta_match;
#echo $resposta_match[0];   

#Acessa ultima URL adicionada usando o padrao abaixo e guarda a resposta numa nova variavel
$acessaedicao = file_get_contents($resposta_match[0]);
$padrao_ultima_edicao = "/(https://online.fliphtml5.com/Agrimidia/\w+/)/";
$procuraII = preg_match($padrao_ultima_edicao, $acessaedicao, $resposta_matchII);

$resposta_matchII;
#echo $resposta_matchII[0];

#Entra na url que faz a requisição para trazer as urls das pages do flip e guarda em uma variavel
$config_js = file_get_contents('https://online.fliphtml5.com/Agrimidia/SI331_digital/files/pageEditor.js?1790620616');
$padrao_html_pages_sem_http = "/(//online.fliphtml5.com/Agrimidia/\w+/files/large/\w+.webp)/";
preg_match_all($padrao_html_pages_sem_http, $config_js, $resposta_proc_pages);
$resposta_proc_pages;
#print_r ($resposta_proc_pages[0]);

$urls_com_https = [];
foreach ($resposta_proc_pages[0] as $key => $edicao) {
    $add_https = "https:".$edicao;
    $urls_com_https[] = $add_https;
   #$sem_fw9 = str_replace("FW9":"", "https", $edicao);
}

#print_r($urls_com_https);

foreach ($urls_com_https as $posicao => $content) {
    $response_url = file_getcontents($content);
    $fliphtml5 = "Página".($posicao+1).".webp";

    if (! empty($response_url)) {
        file_put_contents($fliphtml5, $response_url);
    }
}

print_r(strlen($response_url));

#$url_com_http = "http".$resposta_proc_pages;
#$url_com_http = "http".$resposta_proc_pages;
#$url_com_http = "http".$resposta_proc_pages;
#$url_com_http = "http".$resposta_proc_pages;