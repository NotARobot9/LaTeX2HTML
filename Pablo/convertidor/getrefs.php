<?php 


if (isset($argc)) {
	if (file_exists($argv[1])) {
		$bibfile = fopen($argv[1], "r");
		echo "Leyendo el archivo: " . $argv[1] . "\n\n";
		$bibcontents = explode("\n",stream_get_contents($bibfile));
		$numLineas = count(file($argv[1]));
	}
	else{
		echo "El archivo " . $argv[1] . " no existe.\n";
	}
}

if (isset($argc)) {
	if (file_exists($argv[2])) {
		$contentsFile = fopen($argv[2], "r");
		echo "Leyendo el archivo: " . $argv[2] . "\n\n";
		$contents = stream_get_contents($contentsFile);
		$contentsbyline = explode("\n",$contents);
		$numLineasContentsfile = count(file($argv[2]));
	}
	else{
		echo "El archivo " . $argv[2] . " no existe.\n";
	}
	if (strcmp($argv[3],'')!=0) {
		$outputfile = $argv[3];
	}
	else {
		$outputfile = 'default.html';
	}
}

function contentsReplaceCite() {

	global $numLineasContentsfile;
	global $contentsbyline;
	global $contents;
	global $outputfile;
//	$outputfile = 'pan1_new.html';

	$newcontentsfile = fopen($outputfile,"w");

	$newcontents = preg_replace_callback(
	'/\\\\cite{(\w+)}/', 
		function ($matches) {
			return tag($matches[1]);
		},
		$contents
	);
	fwrite($newcontentsfile, $newcontents);
	fwrite($newcontentsfile, printRefshtmldl());
	fclose($newcontentsfile);
}

function tag($etiqueta) {
	$db = getYear();
	echo "Tag: " . $etiqueta . "\n";
	for ($i=0; $i < count($db); $i++) {
//		echo $db[$i][0];
		if (strcmp($etiqueta, $db[$i][0])==0) {
			return '<a href="#'.$db[$i][0].'">['.$db[$i][3].']</a>';
		}
	}
}

function numeroRefs() {
	global $bibcontents;
	global $numLineas;
	
	$inicioRef = '/\\\\entry/';

	for ($i=0; $i < $numLineas; $i++) { 
		if (preg_match($inicioRef, $bibcontents[$i])) {
			$numRefs++;
		}
	}
	return $numRefs;
}

function leeBiblio() {
	global $bibcontents;
	global $numLineas;
	global $referencia;
	$numRefs =0;

//	echo "El número de líneas es: " .$numLineas. "\n\n";
	$inicioRef = '/\\\\entry\{([^\}]*)\}\{([^\}]*)\}\{([^\}]*)\}/';

	for ($i=0; $i < $numLineas; $i++) {
		if (preg_match($inicioRef, $bibcontents[$i])) {
//			echo $bibcontents[$i];
			$referencia[$numRefs][0]=preg_replace('/^\s+/','',preg_replace($inicioRef, '$1', $bibcontents[$i]));
			$referencia[$numRefs][1]=preg_replace('/^\s+/','',preg_replace($inicioRef, '$2', $bibcontents[$i]));
			$referencia[$numRefs][2]=$i;
			$numRefs++;
		}	
	}
return $referencia;
}

function numtoalpha($num) {

	switch ($num) {
		case '1':
			$alpha = 'a';
			break;
		case '2':
			$alpha = 'b';
			break;
		case '3':
			$alpha = 'c';
			break;
		case '4':
			$alpha = 'd';
			break;
		case '5':
			$alpha = 'e';
			break;
		case '6':
			$alpha = 'f';
			break;
		
		default:
			$alpha = '';
			break;
	}
	return $alpha;
}

function getTags() {

	$numRefs = numeroRefs();	
	$refs = leeBiblio();

	global $numLineas;
	global $bibcontents;
	
	$refs[$numRefs][2] = $numLineas;

	$tagfetch = '/\\\\field{labelalpha}\{([^\}]*)\}/';
	$extratagfetch = '/\\\\field{extraalpha}\{([^\}]*)\}/';

	for ($i=0; $i < $numRefs; $i++) { 
		for ($j=$refs[$i][2]; $j < $refs[$i+1][2]; $j++) { 
			if (preg_match($tagfetch, $bibcontents[$j])) {
				$refs[$i][3] = preg_replace('/^\s+/','',preg_replace($tagfetch, '$1', $bibcontents[$j]));
			}
			if (preg_match($extratagfetch, $bibcontents[$j])) {
				$extratag = numtoalpha(preg_replace('/^\s+/','',preg_replace($extratagfetch, '$1', $bibcontents[$j])));
				$refs[$i][3].=$extratag;
			}
		}
	}
	return $refs;
}

function getAuthors() {
	$numRefs = numeroRefs();
	
	$refs = getTags();
	global $numLineas;
	global $bibcontents;

	$refs[$numRefs][2] = $numLineas;

	$numauthorfetch = '/\\\\name\{author\}{([^}]+)}{}{%/';
	$authorname = '/given=\{([^}]+)\},/';
	$authorlast = '/family=\{([^}]+)\},/';

	for ($i=0; $i < $numRefs; $i++) { 
		for ($j=$refs[$i][2]; $j < $refs[$i+1][2]; $j++) { 
			$temp = '';
			if (preg_match($numauthorfetch, $bibcontents[$j])) {
				$refs[$i][4] = preg_replace('/^\s+/','',preg_replace($numauthorfetch, '$1', $bibcontents[$j]));
				for ($k=0; $k < $refs[$i][4]; $k++) {
					$nombreautor = preg_replace('/^\s+/','',preg_replace($authorname, '$1', $bibcontents[$j + 4 + $k*5]));
					$nombreautor = preg_replace('/\\\\bibnamedelim[a-z]/','',$nombreautor);
					$apellidos = preg_replace('/^\s+/','',preg_replace($authorlast, '$1', $bibcontents[$j + 2 + $k*5]));
					$apellidos = preg_replace('/\\\\bibnamedelim[a-z]/',' ',$apellidos);
					$temp .= $nombreautor . " " . $apellidos;
					if ($refs[$i][4]>1) {
						if ($k<$refs[$i][4]-2) {
							$temp .= ", ";
						} elseif ($k==$refs[$i][4]-2) {
							$temp .= " y ";
						}
					}
					$refs[$i][5] = $temp;
				}
			}
		}
	}
	return $refs;
}

function getTitulo() {
	$numRefs = numeroRefs();
	
	$refs = getAuthors();
	global $numLineas;
	global $bibcontents;

	$titulofetch = '/\\\\field{title}\{([^}]+)\}/';
	for ($i=0; $i < $numRefs; $i++) { 
		for ($j=$refs[$i][2]; $j < $refs[$i+1][2]; $j++) { 
			if (preg_match($titulofetch, $bibcontents[$j])) {
				$refs[$i][6] = preg_replace('/^\s+/','',preg_replace($titulofetch, '$1', $bibcontents[$j]));
			}			
		}
	}
	return $refs;
}

function getJournalNumVolPages() {
	$numRefs = numeroRefs();
	
	$refs = getTitulo();
	global $numLineas;
	global $bibcontents;

	$journalfetch = '/\\\\field{journaltitle}\{([^}]+)\}/';
	$numfetch = '/\\\\field{number}\{([^}]+)\}/';
	$volfetch = '/\\\\field{volume}\{([^}]+)\}/';
	$publisherfetch = '/\\\\list\{publisher\}\{1\}\{%/';
	$thepublisher = '/\{\b([^}]+)\}%/';
	$urlfetch = '/\\\\verb\{urlraw\}/';
	$theurl = '/\\\\verb\s(\w)/';
	$pagesfetch = '/\\\\field{pages}\{(\d+)\\\\bibrangedash\s(\d+)\}/';

	for ($i=0; $i < $numRefs; $i++) { 
		for ($j=$refs[$i][2]; $j < $refs[$i+1][2]; $j++) { 
			if (preg_match($journalfetch, $bibcontents[$j])) {
				$refs[$i][9] = preg_replace('/^\s+/','',preg_replace($journalfetch, '$1', $bibcontents[$j]));
			}
			if (preg_match($numfetch, $bibcontents[$j])) {
				$refs[$i][10] = preg_replace('/^\s+/','',preg_replace($numfetch, '$1', $bibcontents[$j]));
			}
			if (preg_match($volfetch, $bibcontents[$j])) {
				$refs[$i][11] = preg_replace('/^\s+/','',preg_replace($volfetch, '$1', $bibcontents[$j]));
			}
			if (preg_match($publisherfetch, $bibcontents[$j])) {
				$refs[$i][12] = preg_replace('/^\s+/','',preg_replace($thepublisher, '$1', $bibcontents[$j+1]));
			}
			if (preg_match($urlfetch, $bibcontents[$j])) {
				$refs[$i][13] = preg_replace('/^\s+/','',preg_replace($theurl, '$1', $bibcontents[$j+1]));
			}
			if (preg_match($pagesfetch, $bibcontents[$j])) {
				$refs[$i][14] = preg_replace('/^\s+/','',preg_replace($pagesfetch, '$1-$2', $bibcontents[$j]));
			}

		}
	}
	return $refs;
}

function getYear() {
	$numRefs = numeroRefs();
	
	$refs = getJournalNumVolPages();
	global $numLineas;
	global $bibcontents;

	$yearfetch = '/\\\\field{year}\{([^}]+)\}/';
	for ($i=0; $i < $numRefs; $i++) { 
		for ($j=$refs[$i][2]; $j < $refs[$i+1][2]; $j++) { 
			if (preg_match($yearfetch, $bibcontents[$j])) {
				$refs[$i][8] = preg_replace('/^\s+/','',preg_replace($yearfetch, '$1', $bibcontents[$j]));
			}			
		}
	}
	return $refs;
}

function printRefshtml() {
	$db = getYear();

	for ($i=0; $i < count($db)-1; $i++) { 
		$id = $db[$i][0];
		$type = $db[$i][1];
		$tag = $db[$i][3];
		$authors = $db[$i][5];
		$titulo = $db[$i][6];
		$journal = $db[$i][7];
		$year = $db[$i][8];
		$journal = $db[$i][9];
		$number = $db[$i][10];
		$volume = $db[$i][11];
		$publisher = $db[$i][12];
		$url = $db[$i][13];
		$pages = $db[$i][14];

		echo '<div class = "bibentry" id = "' . $id . '">' . "\n";
		echo '<div class = "'.$type.'">' . "\n";

		if (strcmp($type, "article")==0) {
			echo '<span class = "tag">' . $tag . "</span>\n";
			echo '<span class = "authors">' . $authors . "</span>\n";
			echo '<span class = "title">' . $titulo . "</span>\n";
			if (strcmp($journal, '')!=0) {
				echo '<span class = "journal">' . $journal . "</span>\n";
			}		
			if (strcmp($volume, '')!=0) {
				echo '<span class = "volume">' . $volume . "</span>\n";
			}
			if (strcmp($number, '')!=0) {
				echo '<span class = "number">' . $number . "</span>\n";
			}
			// if (strcmp($publisher, '')!=0) {
			// 	echo '<span class = "publisher">' . $publisher . "</span>\n";
			// }

			if (strcmp($pages, '')!=0) {
				$puntuacionyearpages = ",";
			} 
			else { 
				$puntuacionyearpages = ".";
			}

			if (strcmp($year, '')!=0) {
				echo '<span class = "year">(' . $year . ")". $puntuacionyearpages . "</span>\n";
			}			
			if (strcmp($pages, '')!=0) {
				echo '<span class = "pages">' . $pages . ".</span>\n";
			}

		} 
		elseif (strcmp($type, "book")==0) {
			echo '<span class = "tag">' . $tag . "</span>\n";
			echo '<span class = "authors">' . $authors . "</span>\n";
			echo '<span class = "title">' . $titulo . "</span>\n";			

			if (strcmp($publisher, '')!=0) {
				echo '<span class = "publisher">' . $publisher . "</span>\n";
			}

			if (strcmp($pages, '')!=0) {
				$puntuacionyearpages = ",";
			} 
			else { 
				$puntuacionyearpages = ".";
			}

			if (strcmp($year, '')!=0) {
				echo '<span class = "year">' . $year . "". $puntuacionyearpages . "</span>\n";
			}			
			if (strcmp($pages, '')!=0) {
				echo '<span class = "pages">' . $pages . ".</span>\n";
			}
		}  
		elseif (strcmp($type, "misc")==0) {
			echo '<span class = "tag">' . $tag . "</span>\n";
			echo '<span class = "authors">' . $authors . "</span>\n";
			echo '<span class = "title">' . $titulo . "</span>\n";			

			if (strcmp($publisher, '')!=0) {
				echo '<span class = "publisher">' . $publisher . "</span>\n";
			}

			if (strcmp($pages, '')!=0) {
				$puntuacionyearpages = ",";
			} 
			else { 
				$puntuacionyearpages = ".";
			}

			if (strcmp($year, '')!=0) {
				echo '<span class = "year">' . $year. $puntuacionyearpages . "</span>\n";
			}			
			if (strcmp($pages, '')!=0) {
				echo '<span class = "pages">' . $pages . ".</span>\n";
			}
		}
		echo "</div>\n";
		echo "</div>\n\n";
	}
}

function printRefshtmldl() {
	$db = getYear();
	$biblio = '';
		$biblio .= '<dl class="bibliography">'. "\n";

	for ($i=0; $i < count($db)-1; $i++) { 
		$id = $db[$i][0];
		$type = $db[$i][1];
		$tag = $db[$i][3];
		$authors = $db[$i][5];
		$titulo = $db[$i][6];
		$journal = $db[$i][7];
		$year = $db[$i][8];
		$journal = $db[$i][9];
		$number = $db[$i][10];
		$volume = $db[$i][11];
		$publisher = $db[$i][12];
		$url = $db[$i][13];
		$pages = $db[$i][14];


		// echo '<div class = "bibentry" id = "' . $id . '">' . "\n";
		// echo '<div class = "'.$type.'">' . "\n";


		if (strcmp($type, "article")==0) {
			$biblio .= '<dt class = "tag" id = "'.$id.'">' . $tag . "</dt>\n";
			$biblio .= '<dd class="article">' . "\n";
			$biblio .= '<span class = "authors">' . $authors . "</span>\n";
			$biblio .= '<span class = "title">' . $titulo . "</span>\n";
			if (strcmp($journal, '')!=0) {
				$biblio .= '<span class = "journal">' . $journal . "</span>\n";
			}		
			if (strcmp($volume, '')!=0) {
				$biblio .= '<span class = "volume">' . $volume . "</span>\n";
			}
			if (strcmp($number, '')!=0) {
				$biblio .= '<span class = "number">' . $number . "</span>\n";
			}
			// if (strcmp($publisher, '')!=0) {
			// 	echo '<span class = "publisher">' . $publisher . "</span>\n";
			// }

			if (strcmp($pages, '')!=0) {
				$puntuacionyearpages = ",";
			} 
			else { 
				$puntuacionyearpages = ".";
			}

			if (strcmp($year, '')!=0) {
				$biblio .= '<span class = "year">(' . $year . ")". $puntuacionyearpages . "</span>\n";
			}			
			if (strcmp($pages, '')!=0) {
				$biblio .= '<span class = "pages">' . $pages . ".</span>\n";
			}
			if (strcmp($url, '')!=0) {
				$biblio .= '<span class = "url"><a href="' . $url . '">'. $url . "</a></span>\n";
			}
		} 
		elseif (strcmp($type, "book")==0) {
			$biblio .= '<dt class = "tag" id = "'.$id.'">' . $tag . "</dt>\n";
			$biblio .= '<dd class="book">' . "\n";
//				echo '<span class = "tag">' . $tag . "</span>\n";
			$biblio .= '<span class = "authors">' . $authors . "</span>\n";
			$biblio .= '<span class = "title">' . $titulo . "</span>\n";			

			if (strcmp($publisher, '')!=0) {
				$biblio .= '<span class = "publisher">' . $publisher . "</span>\n";
			}

			if (strcmp($pages, '')!=0) {
				$puntuacionyearpages = ",";
			} 
			else { 
				$puntuacionyearpages = ".";
			}

			if (strcmp($year, '')!=0) {
				$biblio .= '<span class = "year">' . $year . "". $puntuacionyearpages . "</span>\n";
			}			
			if (strcmp($pages, '')!=0) {
				$biblio .= '<span class = "pages">' . $pages . ".</span>\n";
			}
		}  
		elseif (strcmp($type, "misc")==0) {
		$biblio .= '<dt class = "tag" id = "'. $id.'">' . $tag . "</dt>\n";
			$biblio .= '<dd class="misc">'."\n";			
//			echo '<span class = "tag">' . $tag . "</span>\n";
			$biblio .= '<span class = "authors">' . $authors . "</span>\n";
			$biblio .= '<span class = "title">' . $titulo . "</span>\n";			

			if (strcmp($publisher, '')!=0) {
				$biblio .= '<span class = "publisher">' . $publisher . "</span>\n";
			}

			if (strcmp($pages, '')!=0) {
				$puntuacionyearpages = ",";
			} 
			else { 
				$puntuacionyearpages = ".";
			}

			if (strcmp($year, '')!=0) {
				$biblio .= '<span class = "year">' . $year. $puntuacionyearpages . "</span>\n";
			}			
			if (strcmp($pages, '')!=0) {
				$biblio .= '<span class = "pages">' . $pages . ".</span>\n";
			}
		}

		$biblio .= "</dd>\n\n";
		// echo "</div>\n";
		// echo "</div>\n\n";
	}
	$biblio .= "</dl>\n";
	return $biblio;
}

//printRefshtml();
printRefshtmldl();

contentsReplaceCite();

//getJournalNumVol();

?>