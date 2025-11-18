# 🇰🇷 Korea Pixel  
**AI로 그리는 한국형 픽셀 아트 생성 서비스**

Korea Pixel은 runwayml/stable-diffusion-v1-5 모델을 기반으로 구축된 **한국 특화 픽셀 아트 생성 웹 서비스**입니다.  
기존 글로벌 모델이 한국의 문화·역사·지리적 요소를 정확하게 표현하지 못하는 문제를 해결하기 위해 개발되었습니다.  
전통문화, 음식, 도시 풍경, 관광지, 인물 등 한국적 디테일을 **512px 픽셀 아트 스타일**로 왜곡 없이 생성하는 것이 핵심 목표입니다.

---

## 빠른 이동
1. [설치 및 실행 (Local Setup)](#-설치-및-실행-local-setup)
2. [Model Info](#Model-Info)
2. [Features](#Features)

---

## Model Info

- **Base Model:** `runwayml/stable-diffusion-v1-5`  
- **Output Resolution:** **512×512**  
- **Training:** LoRA 기반 파인튜닝  
- **Datasets:** 한국 문화 이미지 + 픽셀 아트 데이터 혼합 

---

## 설치 및 실행 (Local Setup)

### 1. 저장소 클론
'''bash
git clone https://github.com/yourusername/korea-pixel.git
cd korea-pixel
'''

---

## Features

### 🎨 한국형 픽셀 아트 생성 (512px)
- 출력 이미지: 512×512
- 픽셀 스타일 기반으로 한국 픽셀 일러스트 생성 
- 전통 건축·랜드마크·도시 풍경 등 다양한 한국 요소 생성  

### 🏞 한국 도시 & 문화 표현 특화
- 서울·부산·경주 등 주요 도시의 상징/랜드마크 학습
- 한국 고유 색감·구조·디자인 요소 반영