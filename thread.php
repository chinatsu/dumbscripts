<?php
	$cache = "api.txt";
	if (file_exists($cache) && (filemtime($cache) > (time() - 60 ))) {
		$file = file_get_contents($cache);
	} else {
		$file = file_get_contents("http://a.4cdn.org/vg/catalog.json");
		file_put_contents($cache, $file);
	}
	$json = json_decode($file, true);
	foreach ($json as $page) {
		foreach ($page['threads'] as $thread) {
			if (preg_match('/\/srg\/|speed ?running/i', $thread['sub'])){
			header("Location: http://4chan.org/vg/res/".$thread['no']);
			/* !!!!!trigger warning!!!!! */
			die;
			}
		}
	}
?>
