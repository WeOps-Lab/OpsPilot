# Web

## WebSocket&Rest

OpsPilot默认开启了5005端口，提供Web端集成，集成的时候，在前端界面加入以下代码，就可以继承了

```
<script>!(function () {
    let e = document.createElement("script"),
        t = document.head || document.getElementsByTagName("head")[0];
    (e.src =
        "https://cdn.jsdelivr.net/npm/rasa-webchat@1.x.x/lib/index.js"),
        // Replace 1.x.x with the version that you want
        (e.async = !0),
        (e.onload = () => {
            window.WebChat.default(
                {
                    customData: {language: "zh"},
                    socketUrl: "http://127.0.0.1:5005",
                    title: "OpsPilot",
                    inputTextFieldHint: "输入...."
                },
                null
            );
        }),
        t.insertBefore(e, t.firstChild);
})();
</script>
```