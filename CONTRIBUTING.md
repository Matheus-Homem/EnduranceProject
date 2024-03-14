<!-- omit in toc -->
# Project Naming Conventions and Commit Guidelines

- [Introduction](#introduction)
- [Branch Naming Conventions](#branch-naming-conventions)
	- [Português](#português)
	- [English](#english)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Conclusion](#conclusion)

## Introduction

This document outlines the naming conventions and commit guidelines to be followed while working on this project. 
Adhering to these conventions will ensure a standardized and clear approach to development.

## Branch Naming Conventions

### Português

Aqui estão as convenções de nomes para utilização nas branches em *pt-br*:

1. **`feat/` (Feature):**
   - Usado para desenvolver novas funcionalidades ou adicionar novos recursos ao projeto;
   - Essas branches geralmente são criadas a partir da branch de desenvolvimento (como develop) e, uma vez concluídas, são integradas de volta a essa branch através de um merge ou rebase;
   - Exemplo: `feat/add-user-authentication`

2. **`chore/` (Chore):**
   - Utilizado para tarefas de manutenção incluindo atualizações de dependências, refatorações de códigos, limpeza de arquivos, ajustes de configuração, entre outros;
   - Essas branches muitas vezes não resultam em alterações visíveis para o usuário final, mas são importantes para manter a qualidade e a saúde geral do código;
   - Exemplo: `chore/update-dependencies`

3. **`docs/` (Documentation):**
   - Destinado a alterações ou adições à documentação do projeto;
   - Isso pode incluir atualizações de README, guias de instalação, documentação de API, notas de lançamento e qualquer outra documentação relevante para os usuários ou desenvolvedores do projeto;
   - Exemplo: `docs/update-readme`

4. **`fix/` (Fix):**
   - Usado para corrigir bugs ou resolver problemas identificados no projeto;
   - As branches de fix geralmente são criadas a partir da branch onde o bug foi identificado (como master ou develop), e uma vez que a correção é implementada, ela é mesclada de volta para essa mesma branch;
   - Exemplo: `fix/resolve-login-issue`

5. **`hotfix/` (Hotfix):**
   - Semelhante à branch de fix, essa prefixo é usado especificamente para correções de bugs críticos que requerem uma correção imediata e não podem esperar até o próximo ciclo de lançamento;
   - Essas correções são geralmente aplicadas diretamente na branch de produção (como master) e também podem ser mescladas de volta para outras branches relevantes, como develop;
   - Exemplo: `style/fix-indentation`

6. **`test/` (Test):**
   - Reservado para branches dedicadas à implementação e execução de testes unitários para garantir a qualidade do código;
   - Exemplo: `test/add-unit-tests`

### English

Here are the conventions for the branch names to use in *en-us*:

1. **`feat/` (Feature):**
   - Used for developing new features or adding new functionality to the project.
   - These branches are usually created from the development branch (such as develop) and, once completed, are merged back into that branch through a merge or rebase.
   - Example: `feat/add-user-authentication`

2. **`chore/` (Chore):**
   - Used for maintenance tasks including updates to dependencies, code refactorings, file cleanups, configuration adjustments, among others.
   - These branches often do not result in visible changes to the end user, but are important for maintaining the overall quality and health of the code.
   - Example: `chore/update-dependencies`

3. **`docs/` (Documentation):**
   - Intended for changes or additions to the project's documentation.
   - This can include updates to README, installation guides, API documentation, release notes, and any other documentation relevant to project users or developers.
   - Example: `docs/update-readme`

4. **`fix/` (Fix):**
   - Used for fixing bugs or addressing identified issues in the project.
   - Fix branches are usually created from the branch where the bug was identified (such as master or develop), and once the fix is implemented, it is merged back into that same branch.
   - Example: `fix/resolve-login-issue`

5. **`hotfix/` (Hotfix):**
   - Similar to the fix branch, this prefix is specifically used for critical bug fixes that require an immediate solution and cannot wait until the next release cycle.
   - These fixes are usually applied directly to the production branch (such as master) and may also be merged back into other relevant branches, such as develop.
   - Example: `hotfix/fix-indentation`

6. **`test/` (Test):**
   - Reserved for branches dedicated to the implementation and execution of unit tests to ensure code quality.
   - Example: `test/add-unit-tests`

## Commit Message Guidelines

1. **Use Clear and Concise Language:**
   - Write commit messages that clearly describe the purpose of the commit in a concise manner.

2. **Use the Present Tense:**
   - Write commit messages in the present tense to describe what the commit does.

3. **Reference Issues:**
   - If the commit relates to a specific issue, reference it in the commit message.

   ```plaintext
   feat: Add new feature

   Resolves #123

4. **Separate Subject from Body:**
   - Separate the subject line from the body of the commit message with a blank line.

   ```plaintext
   feat: Add new feature

   This commit adds a new feature to improve user authentication.

## Conclusion

Following these naming conventions and commit guidelines will contribute to a more organized and understandable version history.
Consistency in naming and committing practices is essential for effective collaboration within the development team.