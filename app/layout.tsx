export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <title>Viva Chefs Assistant</title>
        <meta name="description" content="Chat with Viva Chefs Assistant" />
      </head>
      <body>{children}</body>
    </html>
  )
} 