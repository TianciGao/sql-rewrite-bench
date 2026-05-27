# Witness Design Notes

- The witness keeps one commission value duplicated across different departments, one unique non-null commission, and NULL commissions. That makes the positive rewrite preserve the projected boolean while the negative over-approximates self-matches.
