const fs = require('fs')
const MarkdownIt = require('markdown-it')
const hljs = require('highlight.js')

const md = new MarkdownIt({
    html: true,
    linkify: true,
    typographer: true,
    highlight: (str, lang) => {
        if (lang && hljs.getLanguage(lang)) {
            try {
                return hljs.highlight(str, { language: lang }).value;
            } catch (__) { }
        }

        return ''; // use external default escaping
    }
});

function getDirectories(dir_name) {
    return fs.readdirSync(dir_name, { withFileTypes: true })
        .filter(dirent => dirent.isDirectory()) // only directories
        .map(dirent => dirent.name) // get the name of the directory
        .filter(dir => dir[0] !== '.') // remove hidden directories and node_modules
}

function getReadme(dir_name) {
    const file_name = fs.readdirSync(dir_name, { withFileTypes: true })
        .filter(dirent => dirent.isFile()) // only files
        .map(dirent => dirent.name) // get the name of the file
        .filter(file => file.toLowerCase() === 'readme.md') // get the README.md file
    [0] //  get the first element of the array

    return file_name ? fs.readFileSync(`${dir_name}/${file_name}`, 'utf8') : ''
}

function getTagsFromMd(md_content) {
    // re math example
    // ![wArmup category](https://img.shields.io/badge/Category-Warmups-brightgreen.svg)  
    // ![score](http://img.shields.io/badge/Score_after_CTF-50-blue.svg)  
    // ![solves](https://img.shields.io/badge/Solves-1483-lightgrey.svg) 
    const re_tag = /!\[[a-zA-Z ]+\]\(https?:\/\/[a-zA-Z./\-_0-9%]+.svg\)/gm

    // re math example
    // https://img.shields.io/badge/Category-Warmups-brightgreen.svg  
    // http://img.shields.io/badge/Score_after_CTF-50-blue.svg  
    // https://img.shields.io/badge/Solves-1483-lightgrey.svg
    const re_http = /https?:\/\/[a-zA-Z./\-_0-9%]+.svg/m

    const _tag = md_content.match(re_tag)?.map(item => (item.match(re_http))[0])

    return _tag ? _tag : []
}

function mdToHtml(md_content) {
    return md.render(md_content).replaceAll("\n", "")
}

function getContent(dir_name) {
    const name = dir_name.split(/\\|\//).slice(-1)[0]
    const md = getReadme(dir_name)
    const tags = getTagsFromMd(md)
    const detail = mdToHtml(md)

    let list = []
    const sub_dirs = getDirectories(dir_name)
    for (let dir of sub_dirs) {
        list.push(getContent(`${dir_name}/${dir}`))
    }

    return { name, tags, detail, list }
}

function main() {
    const content = JSON.stringify(getContent(`${__dirname}/write-up`))

    if (fs.existsSync(`${__dirname}/build`)) {
        fs.rmSync(`${__dirname}/build`, { recursive: true })
    }

    fs.mkdirSync(`${__dirname}/build`);
    fs.writeFileSync(`${__dirname}/build/index.json`, content)
}

main()
