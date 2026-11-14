import Foundation
import ScreenCaptureKit
import Darwin

@main
struct WindowScout {
    static func main() async {
        do {
            try await run()
        } catch {
            let message = "Window Scout failed: \(error)\n"
            FileHandle.standardError.write(
                Data(message.utf8)
            )

            exit(1)
        }
    }
    static func run() async throws {
        let allowedBundleIDs: Set<String> = ["com.openai.codex", "com.anthropic.claudefordesktop",]
        let content = try await SCShareableContent
            .excludingDesktopWindows(
            true, onScreenWindowsOnly: true
        )
        let windowInfos = content.windows.compactMap { window -> WindowInfo? in 
            guard let application = window.owningApplication else {
                return nil 
            }

            guard allowedBundleIDs.contains(application.bundleIdentifier) else {
                return nil
            }

            return WindowInfo(
                id: window.windowID,
                application: application.applicationName,
                bundleID: application.bundleIdentifier
            ) 
        }

       let encoder = JSONEncoder()
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]

        let jsonData = try encoder.encode(windowInfos)

        FileHandle.standardOutput.write(jsonData)
        FileHandle.standardOutput.write(Data("\n".utf8))
    }


}

struct WindowInfo: Codable {
    let id: UInt32
    let application: String
    let bundleID: String
}


