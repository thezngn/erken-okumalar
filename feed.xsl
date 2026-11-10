<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8"/>
<xsl:template match="/">
<html lang="tr"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>RSS · Claude ile Erken Okumalar</title><link rel="stylesheet" href="style.css"/></head>
<body><main>
<h1>Claude ile Erken Okumalar</h1>
<p class="sub">Bu bir RSS beslemesi. Adresi Feedly gibi bir RSS okuyucuya eklersen yeni yazılar kendiliğinden gelir:<br/><strong>https://thezngn.github.io/erken-okumalar/feed.xml</strong></p>
<ol class="list">
<xsl:for-each select="rss/channel/item">
<li><a href="{link}"><xsl:value-of select="title"/></a><div class="m"><xsl:value-of select="description"/></div></li>
</xsl:for-each>
</ol>
<p><a href="index.html">← Ana sayfa</a></p>
</main></body></html>
</xsl:template>
</xsl:stylesheet>
