# web_search - Web Search Skill

Perform web searches using various search engines.

## Description

This skill enables web search capabilities using DuckDuckGo, Bing, or other search engines.

## Usage

### Search

```xml
<web_search>
<query>your search query</query>
<num_results>5</num_results>
</web_search>
```

### Parameters

- `query` (required): The search query string
- `num_results` (optional): Number of results to return (default: 5, max: 10)
- `engine` (optional): Search engine to use (default: duckduckgo)

## Examples

```xml
<web_search>
<query>Python tutorial</query>
</web_search>
```

```xml
<web_search>
<query>latest AI news</query>
<num_results>3</num_results>
</web_search>
```

## Response Format

Returns a list of search results with title, URL, and snippet.
