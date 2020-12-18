const request = require('request')

function Resolve(LanzouLink, callback) {
    request(LanzouLink, null, (err, res, body) => {
        if (err) return
        downloadPageUri = SolveDownloadPageUri(body)
        SolveDownloadUrl(downloadPageUri, (downloadUrl) => {
            callback(downloadUrl)
        })
    })
}

function SolveDownloadUrl(downloadPageUrl, callback) {
    request(downloadPageUrl, null, (err, res, body) => {
        let content = body
        let sign = ""
        let signValue = ""
        let data = ""

        // 获取Content中JS部分
        let jsRegex = new RegExp('<script type="text/javascript">\\n([\\S\\s]*?)</script>')
        let jsMatch = content.match(jsRegex)

        if (jsMatch) {
            let jsContent = jsMatch[1]

            // 注释替换表达式
            let descriptionRegex = new RegExp("//.*?[\\n]");
            jsContent = jsContent.replace(descriptionRegex, "\n")

            // 获取data值
            let dataRegex = new RegExp("data : (.*?,'sign':(.*?),.*?})");
            let dataMatch = jsContent.match(dataRegex);

            if (dataMatch) {
                data = dataMatch[1];
                sign = dataMatch[2];

                //根据Sign获取Sign值
                let signRegex = new RegExp("var ajaxdata *?= *?'(.*?)';");
                let signMatch = jsContent.match(signRegex);

                if (signMatch) {
                    signValue = signMatch[1];
                    data = data.replace("'sign':" + sign, "'sign':'" + signValue + "'");
                }
            }
        }

        //转化data为键值对
        // data = Json2FormData(data)
        // data = Encoding.UTF8.GetString(Encoding.Default.GetBytes(data))
        // let phpContent = PostAjax(data, downloadPageUrl)

        let r = request.post(downloadPageUrl, null, (error, response, body) => {
            if (!error && response.statusCode == 200) {
                let phpContent = body
                let finalUrl = "";
                let domRegex = new RegExp("\"dom\":\"(.*)\",\"url\"")
                let urlRegex = new RegExp("\"url\":\"(.*)\",\"inf\"")

                let domMatch = phpContent.match(domRegex)
                let urlMatch = phpContent.match(urlRegex)

                if (domMatch) {
                    finalUrl = domMatch[1].replace("\\", "")
                }

                finalUrl += "/file/"
                if (urlMatch) {
                    finalUrl += urlMatch[1].replace("\\", "")
                }

                callback(finalUrl)
            }
        })

        let form = r.form()
        data = JSON.parse(data.replace(/'/g, '"'))
        Object.keys(data).forEach((key) => {
            form.append(key, data[key])
        })

    })
}

function SolveDownloadPageUri(content) {
    let regex = new RegExp("<iframe class=\"ifr2\" name=\"[0-9]+\" src=\"((.+))\" frameborder=\"0\" scrolling=\"no\"></iframe>\n")
    let match = content.match(regex)
    let relativeUrl = ''
    if (match) {
        relativeUrl = match[1]
    }

    if (relativeUrl !== '') {
        return "https://sdchao.lanzous.com" + relativeUrl
    }
    else
        return null
}


Resolve("https://wwe.lanzous.com/i9T15jhtm0h", (url) => {
    console.log(url)
})
