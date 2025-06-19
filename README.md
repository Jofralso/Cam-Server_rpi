Aqui está um **README.md** polido e completo para o teu projeto `cam-server`, com instruções claras para setup, uso e deploy. Podes copiá-lo para o repositório no GitHub:

````markdown
# 📸 Cam‑Server com Inky pHAT

Projeto para Raspberry Pi Zero 2 W (DietPi) com:
- Módulo de câmara CSI (OV5640)
- Inky pHAT como display de estado
- LED RGB + botão físico para interação
- Servidor web para galeria de fotos e GIFs

---

## 🔧 Instalação

Requisitos no host (Raspberry Pi com SPI/I²C ativos):
```bash
sudo apt update
sudo apt install -y libcamera-apps python3-libcamera python3-pip
````

No projeto (via Docker ou pip em VENV):

```bash
pip install -r requirements.txt
```

---

## 🚀 Em desenvolvimento (via Docker)

```bash
docker-compose up --build -d
```

Acede em \<http\://<IP do Pi>:8000>.

---

## 🧪 Testes sem Docker

1. Ativa ambiente virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Arranca manualmente:

   ```bash
   python3 app.py
   ```

---

## 🧰 Hardware & conexões

| Item      | Pinos GPIO (BCM)                                                             | Função           |
| --------- | ---------------------------------------------------------------------------- | ---------------- |
| LED RGB   | 22 (R), 27 (G), 17 (B)                                                       | Status           |
| Botão     | 5 (pull-up)                                                                  | Ações: foto, GIF |
| Inky pHAT | SPI0 + I²C (sem conflito de CS — `dtoverlay=spi0-0cs` no `/boot/config.txt`) |                  |

---

## 🎛️ Como funciona

* **Botão**:

  * Pressão curta → tira foto
  * Pressão longa → cria GIF (5 imagens)

* **LED RGB**:

  * Verde → pronto
  * Amarelo → a tirar foto
  * Azul → a criar GIF
  * Vermelho → servidor parado

* **Inky pHAT** acusa o estado atual e número de itens.

* **Servidor web**:

  * `/` → galeria de fotos e GIFs
  * `/photos/<nome>` → serve ficheiro
  * `/api/status` → devolve JSON com contadores

---

## 🌟 Exemplos de uso

* **Tira uma foto**: pressiona botão (LED fica amarelo), Inky atualiza contagem.
* **Cria um GIF**: mantém pressionado (LED azul), Inky indica “GIF!”.
* **Visualiza galerias**: acede via browser ao IP:8000.

---

## 🌐 Referências

* Projeto similar: Flask + transmissão de câmara via Pi (<339⭐) ([adambowie.com][1], [github.com][2], [github.com][3])
* Implementação Inky pHAT com SPI/I²C (`dtoverlay=spi0-0cs`)&#x20;

---

## 🛠️ Próximos passos

* Adicionar **streaming de vídeo ao vivo**
* Suporte a **backup automático** (ex: Dropbox ou Google Drive)
* Diferentes **modos de botão**:

  * Pressão dupla para reiniciar
  * Pressão longa para desligar via libcamera ou systemd

---

> Feito com ❤️ para automação simples com interface física e web.

[1]: https://www.adambowie.com/blog/2019/09/news-twitter-feeds-and-inky-what-e-ink-display/?utm_source=chatgpt.com "News Twitter Feeds and Inky WHAT E-Ink Display – adambowie.com"
[2]: https://github.com/pimoroni/inky/blob/master/README.md?utm_source=chatgpt.com "inky/README.md at main · pimoroni/inky - GitHub"
[3]: https://github.com/pimoroni/inky?utm_source=chatgpt.com "pimoroni/inky: Combined library for V2/V3 Inky pHAT and Inky wHAT."
