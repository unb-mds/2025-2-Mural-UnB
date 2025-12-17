import {
  HeroSection,
  AboutSection,
  AccessMuralButton,
  CarouselSection,
  InfoBanner
} from "./components"

export default function Home() {
  return (
    <div className="flex flex-col items-center">
      <HeroSection />
      <AboutSection />
      <AccessMuralButton />
      <CarouselSection />
      <InfoBanner />
    </div>
  )
}