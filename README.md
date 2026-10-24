# 쌀양이의 지식국밥 – 링크 모음

https://soso1sangssalyang.github.io/

정적 페이지(빌드 없음): `index.html`, `style.css`, `app.js`, 데이터는 `data/posts.json`.
비밀값·트래커 없음. 폰트만 jsDelivr CDN(Pretendard)에서 불러옵니다.

## posts.json 형식 (최신순)
```json
[{"id":"slug","title":"제목","date":"YYYY-MM-DD","thumbnail":"assets/x.jpg (선택)",
  "youtube_url":"https://www.youtube.com/watch?v=...",
  "products":[{"name":"상품명","url":"https://link.coupang.com/a/...","note":"한줄 메모"}]}]
```
- 상품 링크는 `rel="sponsored nofollow noopener"`, `target="_blank"`로 렌더링됩니다.
- 상품이 있는 게시물이 하나라도 있을 때만 쿠팡 파트너스 고지문이 섹션 상단에 표시됩니다.
- 상품이 없는 게시물(예: 주류 주제)은 제목 + 유튜브 링크만 보입니다.

## add_post.py (게시물 추가/수정 → 자동 commit & push)
```bash
# 새 게시물
python3 add_post.py --id my-post --title "제목" --date 2026-10-27 \
  --youtube "https://www.youtube.com/watch?v=XXXX" --thumbnail assets/thumb-my-post.jpg

# 상품 추가 (여러 개 가능, URL 중복은 무시)
python3 add_post.py --id my-post \
  --product "상품명|https://link.coupang.com/a/xxxx|한줄 설명" \
  --product "상품2|https://link.coupang.com/a/yyyy|"

# 상품 목록 통째로 교체 / 게시물 삭제
python3 add_post.py --id my-post --replace-products --product "..."
python3 add_post.py --id my-post --delete
```
옵션: `--no-push`(커밋만), `--dry-run`(JSON 출력만). 썸네일 이미지는 `assets/`에 먼저 넣어두면 같이 커밋됩니다.
실제로 생성한 쿠팡 파트너스 링크만 넣으세요.
