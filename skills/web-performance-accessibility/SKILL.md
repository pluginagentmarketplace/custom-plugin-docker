---
name: web-performance-accessibility
description: Master web performance optimization and accessibility standards. Learn Core Web Vitals, image optimization, code splitting, and WCAG compliance.
sasmp_version: "1.3.0"
bonded_agent: 01-frontend-web-development
bond_type: PRIMARY_BOND
---

# Web Performance & Accessibility

Optimize for speed and inclusive user experience.

## Core Web Vitals

```typescript
// Largest Contentful Paint (LCP) - Perceive speed
// Target: < 2.5s
// Optimize: Image loading, preload fonts, lazy load below-fold

// First Input Delay (FID) → Interaction to Next Paint (INP)
// Target: < 100ms
// Optimize: Break up JS, use requestAnimationFrame, Workers

// Cumulative Layout Shift (CLS)
// Target: < 0.1
// Optimize: Fixed dimensions, animations with transform

// Measure in React
useEffect(() => {
  const handleMetric = (metric: any) => {
    console.log(metric.name, metric.value)
  }

  import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
    getCLS(handleMetric)
    getFID(handleMetric)
    getFCP(handleMetric)
    getLCP(handleMetric)
    getTTFB(handleMetric)
  })
}, [])
```

## Image Optimization

```html
<!-- Use modern formats with fallbacks -->
<picture>
  <source srcset="image.webp" type="image/webp" />
  <source srcset="image.jpg" type="image/jpeg" />
  <img src="image.jpg" alt="Description" loading="lazy" />
</picture>

<!-- Responsive images -->
<img
  srcset="small.jpg 480w, medium.jpg 960w, large.jpg 1920w"
  sizes="(max-width: 480px) 480px, (max-width: 960px) 960px, 1920px"
  src="medium.jpg"
  alt="Responsive image"
/>

<!-- Priority hints -->
<link rel="preload" as="image" href="hero.webp" />
<link rel="prefetch" href="lazy.jpg" />
```

## Code Splitting

```typescript
// Route-based code splitting
const Home = lazy(() => import('./pages/Home'))
const About = lazy(() => import('./pages/About'))

// Component-level splitting
const HeavyChart = lazy(() => import('./components/Chart'))

export function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </Suspense>
  )
}
```

## Accessibility (WCAG 2.1)

```html
<!-- Semantic HTML -->
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>

<!-- Form accessibility -->
<label htmlFor="name">Name:</label>
<input id="name" type="text" aria-required="true" />

<!-- Images -->
<img src="chart.png" alt="Sales increased 20% in Q3" />

<!-- ARIA when needed -->
<button
  aria-label="Close menu"
  aria-expanded="false"
  aria-controls="menu"
  onClick={toggleMenu}
>
  ☰
</button>

<!-- Keyboard navigation -->
<div role="tablist">
  <button role="tab" aria-selected="true" tabIndex="0">Tab 1</button>
  <button role="tab" aria-selected="false" tabIndex="-1">Tab 2</button>
</div>
```

## Font Optimization

```css
/* System fonts (fastest) */
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Web fonts with optimal loading */
@font-face {
  font-family: 'CustomFont';
  src: url('font.woff2') format('woff2');
  font-display: swap; /* Shows fallback immediately */
}
```

## Monitoring

```typescript
// PageSpeed Insights API
const response = await fetch(
  `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=${url}&key=${API_KEY}`
)

// Lighthouse in CI/CD
// npm install --save-dev @lhci/cli@0.9.x @lhci/github-check-reporter@0.9.x

// WebPageTest API
const testUrl = `https://www.webpagetest.org/runtest.php?url=${url}`
```

## Best Practices

1. **Performance**: Lazy load images, defer JS, preload critical resources
2. **Accessibility**: Use semantic HTML, ARIA when needed, keyboard navigation
3. **Testing**: Run Lighthouse, test with screen readers, keyboard-only navigation
4. **Monitoring**: Set Core Web Vitals budgets, track metrics over time
5. **Images**: Serve modern formats, responsive images, descriptive alt text
6. **Fonts**: Use system fonts or limit web fonts, font-display: swap
7. **JavaScript**: Code split, minify, tree-shake unused code
8. **Analytics**: Track real user metrics with web-vitals library

## Testing Tools

- Lighthouse: Built into Chrome DevTools
- WebPageTest: https://www.webpagetest.org
- WAVE: Web accessibility evaluator
- axe DevTools: Accessibility testing
- PageSpeed Insights: Google's analysis tool
