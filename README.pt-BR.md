# Davi Luis

[🇺🇸 English](README.md) · 🇧🇷 Português

**Desenvolvedor full stack do Rio de Janeiro. Construo sistemas que rodam no mundo real, de APIs e aplicações web a integrações com hardware e visão computacional.**

> *Código é uma forma de pensar.* Escrevo software do jeito que tento viver: com clareza, sem atalhos e pensando em quem vem depois.

Boa parte do meu trabalho acontece longe do navegador. Um carro para no portão, a câmera lê a placa e o meu código tem algumas centenas de milissegundos para decidir se o portão abre. Meu dia a dia é com câmeras de leitura de placas, controladoras de acesso, bancos Firebird legados e servidores Windows em condomínios, onde não tem ninguém por perto para reiniciar nada. Isso me ensinou a cuidar da parte chata: modos de falha, testes e atualizações que se desfazem sozinhas quando algo dá errado.

[Portfólio](https://portifolio-daviluissantos-projects.vercel.app/) · [LinkedIn](https://www.linkedin.com/in/davi-luis/) · [YouTube](https://www.youtube.com/channel/UCryhrvnlMcEfvisWyQurlyA) · [Instagram](https://www.instagram.com/davi.luissc/)

---

## O que eu construí

### 🚗 Servidor LPR de controle de acesso veicular · *em produção*
Servidor .NET on-premise, feito para a Segmix, que decide em tempo real quais veículos podem entrar em condomínios residenciais.
- Integra **cinco fabricantes de câmeras, cada um com seu protocolo**: Alphadigi (HTTP, TCP binário, JSON-RPC), Hikvision, Motorola, Intelbras e antenas UHF Control iD. Um teste de arquitetura impede que código de fabricante vaze para o núcleo.
- **Saindo do sistema legado:** um modo novo roda sem o sistema Delphi/Firebird ao lado do qual o servidor nasceu. Veículos, unidades, direitos de vaga e histórico de acessos vêm da plataforma que está substituindo esse sistema, e cada passagem fica guardada em disco até ser entregue.
- **Fail-closed por design:** na dúvida, o portão fica fechado. As placas autorizadas também são sincronizadas em cada câmera, então o portão continua funcionando se o servidor cair.
- **Operação que se recupera sozinha:** detecta câmeras que pararam de enviar eventos e as reconfigura, e se atualiza numa janela de manutenção, com rollback automático se o health check falhar.
- **1.500+ testes automatizados** (incluindo testes de contrato contra um Firebird real no Docker) e **95+ releases**. O código é privado; os builds saem por um [repositório público de releases](https://github.com/DaviLuisSantos/AlphadigiServidorLPR-releases).

`.NET 10` `ASP.NET Core` `Firebird` `SQLite` `MediatR` `GitHub Actions`

### 🔐 [ControlId.Net](https://github.com/DaviLuisSantos/ControlId.Net) · *open source, no [NuGet](https://www.nuget.org/packages/ControlId.Net)*
A biblioteca .NET que eu queria que existisse quando comecei a integrar equipamentos de acesso e relógios de ponto REP da Control iD.
- Cobre toda a API documentada da linha de acesso (iDAccess, iDFlex, iDFace, iDBox, iDUHF), de usuários, faces e catracas a interfonia SIP, streaming RTSP e configurações de rede, com um teste que falha se alguma seção documentada ficar de fora.
- Feita para vários equipamentos ao mesmo tempo: operações em lote com resultado por equipamento, leitura paginada com `IAsyncEnumerable` e limite de requisições simultâneas por equipamento, calibrado num iDFace real.
- Sessão gerenciada com re-login automático, modo Push para equipamentos atrás de NAT e endpoints ASP.NET Core para autorizar acessos em tempo real.
- Parser em streaming de arquivos AFD (Portaria 671/2021 e 1510/2009) que valida CRC-16 e não para de ler quando encontra linhas corrompidas.
- **220+ testes** rodando em .NET 8 e .NET 10 (Linux) e .NET Framework 4.8 (Windows). Três pacotes no NuGet (núcleo, DependencyInjection e AspNetCore) publicados com Trusted Publishing (OIDC): nenhuma chave no repositório, e nada é publicado se algum teste falhar.

`.NET 8` `.NET 10` `.NET Standard 2.0` `ASP.NET Core` `xUnit`

### 📟 [CYD PC Dashboard](https://github.com/DaviLuisSantos/cyd-pc-dashboard) · *firmware ESP32*
Uma telinha touch de US$15 ao lado do monitor mostrando status do PC, processos, rede, verificação de serviços, cotações com histórico de 24h, o que está tocando (com controles), botões de atalho que rodam ações no PC e estatísticas do YouTube. [Grave o firmware pelo navegador](https://daviluissantos.github.io/cyd-pc-dashboard/), sem instalar nada.
- Renderização sem flicker com sprites fora da tela, temas de cor, modo noturno, LED RGB de status, brilho automático pelo sensor de luz e interface em português e inglês.
- Atualização pelo Wi-Fi (OTA) que volta sozinha para a versão anterior se o firmware novo não ficar saudável, interface web e um agente no PC que a tela encontra sozinha na rede, distribuído também como `.exe` para Windows, sem precisar de Python.
- A parte divertida foi depurar o hardware: leituras SPI corrompidas porque a tela e o touch dividiam o mesmo periférico, e leituras do framebuffer deslocadas em um bit até eu baixar o clock de leitura para 6 MHz.

`C++` `ESP32` `PlatformIO` `Python` `GitHub Actions`

### Outros
- **Arco** (privado, segunda geração): PWA de hábitos que evoluem, com níveis, objetivos em ciclos de 6 semanas, XP e conquistas. .NET 10 e React 19 num único processo, fila de check-ins offline, Web Push feito do zero e um servidor MCP para assistentes de IA registrarem hábitos. A [primeira versão](https://github.com/DaviLuisSantos/HabitSystem) (.NET 9 + Next.js) está arquivada.
- **Emplaca** (privado por enquanto, *alfa*): o meu próprio reconhecimento de placas brasileiras, com detector e OCR treinados em PyTorch e rodando nativamente no .NET via ONNX Runtime, em CPU. Detector sem âncoras, decodificador sintático para placas Mercosul e antigas, gerador sintético de placas e testes de paridade Python ↔ .NET. Rodar o detector só onde cada câmera de fato vê placas cortou 37% do tempo por quadro, com a mesma precisão.
- **[JobRadar AU](https://github.com/DaviLuisSantos/job-radar-au)**: acompanha o mercado de trabalho australiano para quem chega com visto de Working Holiday. Coleta vagas todo dia, ranqueia cada uma contra um perfil com uma nota que se explica, acompanha candidaturas e monta um retrato mensal agregado do mercado para uma newsletter para brasileiros indo para a Austrália. É a reescrita em .NET 10 do meu protótipo em Python, o [Job Tracker](https://github.com/DaviLuisSantos/job-tracker), conferida para dar as mesmas notas em 5.388 vagas reais. Arquitetura em camadas, Postgres, tela de triagem em Blazor, rodando como serviços do Windows.
- **Pipeline de pesquisa para o YouTube** (privado): baixa as legendas dos vídeos ou, quando o YouTube limita as requisições, transcreve o áudio localmente com faster-whisper, e usa LLMs para analisar as transcrições e extrair insights para o meu canal. Roda por uma pequena interface web.
- **[Roteiro Manager](https://github.com/DaviLuisSantos/RoteiroManager)**: o editor de Markdown com teleprompter que eu uso para gravar meus próprios vídeos.

---

## Como eu trabalho

- **Parto do princípio de que vai dar errado.** A rede cai, a câmera trava, o banco dá lock. Projeto pensando nisso primeiro: padrão fail-closed, retry com backoff, health check, rollback.
- **Teste é o que me deixa fazer deploy na sexta.** A maior parte do código que importa roda onde eu não alcanço, então a suíte de testes é a minha rede de segurança.
- **Fronteiras mantêm o código honesto.** Protocolos de fabricante, frameworks e banco ficam nas bordas, e deixo testes de arquitetura garantirem isso.
- **Números acima de impressões.** Meço modelos em dados que eles nunca viram, mostro o que o limiar de confiança realmente entrega e deixo claro o que ainda não foi medido.
- **Release automatizado.** Tag, build, teste, publicação, atualização. Se depende de alguém lembrar um passo, uma hora esse passo é esquecido.

## Ferramentas que eu uso

- **Back end:** C# / .NET, ASP.NET Core, EF Core, MediatR, Node.js
- **Front end:** TypeScript, React, Next.js, Blazor, Astro, Tailwind CSS
- **IA e visão computacional:** PyTorch, ONNX / ONNX Runtime, OpenCV, detecção de objetos e OCR, geração de dados sintéticos, Whisper (speech-to-text), APIs de LLM
- **Dados:** PostgreSQL, SQLite, Firebird
- **Cloud e DevOps:** Azure, Docker, GitHub Actions
- **Também:** Python, ESP32 / PlatformIO

## GitHub em números

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="profile-summary-card-output/github_dark/0-profile-details.svg" />
  <img alt="Profile details" src="profile-summary-card-output/github/0-profile-details.svg" width="100%" />
</picture>
</p>

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="profile-summary-card-output/github_dark/3-stats.svg" />
  <img alt="GitHub stats" src="profile-summary-card-output/github/3-stats.svg" width="49%" />
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="profile-summary-card-output/github_dark/4-productive-time.svg" />
  <img alt="Productive time" src="profile-summary-card-output/github/4-productive-time.svg" width="49%" />
</picture>
</p>

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="profile-stats/releases-dark.svg" />
  <img alt="Releases shipped" src="profile-stats/releases-light.svg" width="49%" />
</picture>
</p>

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="profile-summary-card-output/github_dark/1-repos-per-language.svg" />
  <img alt="Repos per language" src="profile-summary-card-output/github/1-repos-per-language.svg" width="49%" />
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="profile-summary-card-output/github_dark/2-most-commit-language.svg" />
  <img alt="Most commit language" src="profile-summary-card-output/github/2-most-commit-language.svg" width="49%" />
</picture>
</p>

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/DaviLuisSantos/DaviLuisSantos/output/github-snake-dark.svg" />
  <img alt="Cobrinha comendo meu gráfico de contribuições" src="https://raw.githubusercontent.com/DaviLuisSantos/DaviLuisSantos/output/github-snake.svg" />
</picture>
</p>

## Além do código

Sou formado em Análise e Desenvolvimento de Sistemas, curso Ciência da Computação e tenho a certificação **Microsoft Certified: Azure Fundamentals (AZ-900)**. No meu canal do YouTube, o **Davi Dev**, mostro os projetos que estou construindo, as ferramentas que uso e o que venho aprendendo no caminho.

[**Assistir no YouTube →**](https://www.youtube.com/channel/UCryhrvnlMcEfvisWyQurlyA)
