# ReadAI-OCR

Aplicação para leitura e extração de informações de documentos utilizando OCR.

O projeto foi criado para estudar, na prática, um fluxo de processamento de documentos envolvendo **OCR, processamento local, APIs e inteligência artificial**, mantendo a aplicação simples e separada por responsabilidades.

## Arquitetura

A aplicação foi organizada separando o recebimento das requisições, o processamento do OCR, a extração dos dados e a futura integração com IA.

Essa escolha não é apenas uma questão de organização do código. Ela permite controlar **onde cada etapa do processamento acontece**.

### Por que processar localmente?

O OCR é realizado localmente utilizando o Tesseract.

Isso permite que o documento seja processado inicialmente dentro do próprio ambiente da aplicação, evitando enviar automaticamente todo o conteúdo para um serviço externo.

Essa abordagem pode trazer benefícios em três pontos:

**Custos**

O processamento básico do documento não depende de uma chamada de API para cada arquivo. A API de IA pode ser utilizada somente quando uma análise mais avançada for necessária.

**Privacidade**

Documentos podem conter informações pessoais ou sensíveis. Manter o processamento inicial local reduz a necessidade de enviar o documento completo para terceiros.

A arquitetura foi pensada considerando requisitos de privacidade e proteção de dados, especialmente em cenários que envolvam dados pessoais e a LGPD.

> O uso de processamento local não significa, por si só, que uma aplicação esteja automaticamente em conformidade com a LGPD. A conformidade depende também de fatores como finalidade, tratamento, armazenamento, segurança, controle de acesso e demais requisitos aplicáveis ao cenário.

**Flexibilidade**

A aplicação pode realizar o processamento básico localmente e utilizar uma API externa apenas para tarefas que realmente necessitem de inteligência artificial.

Dessa forma:

```text
Documento
   ↓
OCR local
   ↓
Extração local
   ↓
Precisa de análise inteligente?
   │
   ├── Não → Finaliza
   │
   └── Sim
         ↓
      API de IA
```

Essa separação também permite substituir o provedor de IA futuramente sem precisar alterar o funcionamento do OCR ou do controller.

## Tecnologias

* Python
* Flask
* Tesseract OCR
* Pillow
* Docker

### Organização

**controller**

Responsável por receber as requisições e organizar o fluxo da aplicação.

**service/ocr.py**

Responsável pela leitura do documento utilizando Tesseract OCR localmente.

**service/extrator.py**

Responsável por procurar no texto os campos definidos pelo usuário.

**service/ia.py**

Responsável pela futura integração com uma API de inteligência artificial.

A separação permite que o provedor de IA seja alterado sem modificar o OCR ou a camada responsável pelas requisições.


## Próximos passos

* Integração com API de inteligência artificial
* Envio somente do conteúdo necessário para análise
* Análise inteligente dos dados extraídos
* Identificação mais flexível dos campos
* Suporte a diferentes tipos de documentos
* Melhor tratamento para documentos em PDF
* Validação dos dados encontrados


> **Processar localmente o que puder ser processado localmente e utilizar serviços externos somente quando agregarem valor ao processamento.**
