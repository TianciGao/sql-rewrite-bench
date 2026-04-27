# PERF_0105 Schema Notes

- The witness retains the company, country-info, rating-info, keyword, and title tables needed by the violent western movie family.
- `movie_companies.note` is kept as text because the source query depends on simple `LIKE` matching of release-window style annotations.
- The witness uses one `violence` row and one `murder` row so the narrower negative keyword set changes the aggregate outcome without relying on null behavior.
