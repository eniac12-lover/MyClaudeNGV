TEMPLATE STATUS: PROVIDED

> 공식 다이어그램 템플릿: `WP_Templates/Engineering/SoftwareDetailedDesignAndUnitConstruction/TPL-SWE3-002_상세설계 UML 및 호출관계 템플릿.drawio`
>
> ⚠️ 동일한 저작권/이용 제한이 적용됩니다(`references/detailed-design-template.md` 상단 참고).

## 절차

1. 템플릿을 `<산출물 ID>_<산출물명>.drawio`로 복사합니다(원본 수정 금지).
2. `WP_Templates/Engineering/README.md` 지침대로 안내 도형(제목 "작성 안내"가 있는 노란 박스, 예시 액터/요소/화살표)을 **삭제**하고 실제 구현 단위, 액터/외부 요소, 인터페이스·호출 관계, 추적 ID로 채웁니다.
3. 복잡한 호출관계는 먼저 Mermaid로 초안을 그려 구조를 검증한 뒤(`architecture-design`의 `references/architecture-diagrams.md` 문법 재사용), 최종본만 drawio로 옮깁니다. 초안 Mermaid는 채팅/중간 산출물로만 쓰고, 공식 산출물은 반드시 drawio 파일입니다.
4. 검토본/베이스라인을 만들 때는 PNG로 함께 내보냅니다(README 지침).

## drawio XML 직접 작성/편집 방법 (GUI 없이)

drawio 파일은 일반 XML이므로 `Read`/`Edit`/`Write`로 직접 다룰 수 있습니다. `mxCell` 하나가 도형(vertex) 또는 관계선(edge) 하나입니다.

- 노드(vertex): `<mxCell id="..." value="라벨" style="..." vertex="1" parent="1"><mxGeometry x=".." y=".." width=".." height=".." as="geometry"/></mxCell>`
- 관계선(edge): `<mxCell id="..." value="인터페이스/관계명" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;" edge="1" parent="1" source="노드ID" target="노드ID"><mxGeometry relative="1" as="geometry"/></mxCell>`
- 여러 도형을 겹치지 않게 배치하려면 `x`/`y`/`width`/`height`를 기존 도형과 충돌하지 않는 좌표로 계산합니다(대략 격자 간격 160~200 권장).
- 모든 관계선에는 `value`에 인터페이스 ID/이름 또는 호출 관계명을 명시합니다(라벨 없는 연결 금지 — `architecture-design`의 인터페이스 전용 통신 원칙을 상세설계에서도 유지).

## 검토 체크리스트

- [ ] 안내 도형(노란 박스, 예시 라벨)이 모두 삭제되고 실제 내용으로 대체되었는가?
- [ ] 모든 연결선에 인터페이스/호출 관계 라벨이 있는가?
- [ ] 구현 단위 ID가 `references/detailed-design-template.md` §2(모듈 분해)의 `UNIT-nnn`과 일치하는가?
- [ ] 베이스라인 시점에 PNG 내보내기를 완료했는가?
