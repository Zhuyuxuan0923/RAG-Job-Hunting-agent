# Agentic RAG Job Assistant SaaS UI Redesign

## Goal

Improve the frontend visual quality so the product feels like a credible, modern SaaS workbench for AI-assisted job preparation. Preserve the existing workflow and backend contracts while making the UI clearer, more polished, and fully readable in Chinese.

## Current Problems

- Many visible Chinese strings are mojibake, including navigation, page titles, buttons, and helper text.
- The visual system is functional but basic: generic cards, repeated gradients, light hierarchy, and limited page rhythm.
- Report pages do not yet feel like analysis workspaces.
- The interview page works structurally but can feel like a simple chat demo instead of a guided interview cockpit.

## Visual Direction

Use a professional SaaS tool style:

- Clean light interface with a subtle cool background, white surfaces, and restrained blue/teal accents.
- Strong but quiet hierarchy: clear page titles, short supporting copy, compact status indicators, and scannable sections.
- Consistent card, table, button, tag, progress, and empty/loading states.
- No marketing-style landing page. The first screen remains the actual upload workflow.
- Avoid heavy decoration, excessive gradients, and repeated card grids where a report/table layout is clearer.

## Scope

### Global App Shell

- Replace mojibake brand/navigation text with readable Chinese.
- Upgrade the sticky header with a compact product mark, product name, and workflow-aware navigation affordances.
- Refresh global CSS variables: colors, typography, radii, shadows, spacing, focus states, and responsive layout.
- Keep the existing Vue Router structure.

### Upload Page

- Keep the two-column resume/JD upload model on desktop and a stacked layout on mobile.
- Make the page read as a workbench start screen: concise title, workflow steps, two clear upload panels, and a strong primary action.
- Improve uploaded states with calm success styling, filename/preview readability, and reset controls.
- Fix all visible Chinese copy.

### Match Report

- Turn the match result into an analysis dashboard:
  - score hero with concise summary,
  - company/interview/skills/preparation cards,
  - polished skill comparison table,
  - improvement suggestions as readable action items.
- Preserve existing data fields and streaming thinking display.
- Fix loading, error, CTA, and table copy.

### Interview Page

- Present the start state as a guided interview setup panel.
- Present the active state as a focused interview workspace with a clear status bar, chat stream, question cards, feedback blocks, and answer input.
- Preserve the current message flow and API calls.
- Fix all visible Chinese copy, including skipped answers and completion state.

### Interview Report

- Keep the existing score summary, question review, weak-area analysis, and study plan sections.
- Improve section spacing, headings, surface styling, and return action.
- Fix loading and navigation copy.

## Component Strategy

- Prefer updating existing Vue components and shared CSS over introducing a new UI framework.
- Reuse current components such as `FileDropZone`, `TextPasteArea`, `InfoCard`, `ScoreCircle`, `ChatBubble`, `QuestionCard`, `FeedbackCard`, `AnswerInput`, `ScoreSummary`, `WeakAreaAnalysis`, and `StudyPlan`.
- Add small shared visual primitives only if they reduce duplication across pages.
- Keep icons as inline SVGs or existing local patterns; do not add a dependency unless the existing implementation becomes cumbersome.

## Accessibility And Responsive Behavior

- Maintain keyboard focus visibility for buttons, links, inputs, and upload controls.
- Ensure text does not overflow on mobile.
- Use responsive grids that collapse predictably below tablet width.
- Keep contrast suitable for normal body text, table labels, and disabled states.

## Testing And Verification

- Run the frontend build command.
- Start the Vite dev server and inspect the UI in a browser.
- Verify desktop and mobile layouts for:
  - upload page,
  - match report loading/result states where possible,
  - interview start and active states where possible,
  - interview report loading/result states where possible.
- Confirm there is no visible mojibake in edited frontend files.

## Out Of Scope

- Backend API changes.
- New authentication, persistence, or user account features.
- Reworking the interview or matching algorithms.
- Replacing the app with a marketing landing page.
