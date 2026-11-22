import CoreImage
import Foundation
import Vision

enum MaskError: LocalizedError {
    case usage
    case noFrames
    case outputNotEmpty
    case unreadableFrame(String)

    var errorDescription: String? {
        switch self {
        case .usage:
            return "Usage: foreground-masks INPUT_PNG_DIRECTORY OUTPUT_DIRECTORY"
        case .noFrames:
            return "The input directory contains no PNG frames."
        case .outputNotEmpty:
            return "Choose a new or empty output directory."
        case .unreadableFrame(let name):
            return "Could not read frame \(name)."
        }
    }
}

@available(macOS 14.0, *)
func generateMasks(input: URL, output: URL) throws {
    let files = FileManager.default
    let frames = try files.contentsOfDirectory(
        at: input, includingPropertiesForKeys: [.isRegularFileKey], options: .skipsHiddenFiles
    ).filter {
        $0.pathExtension.lowercased() == "png" &&
            (try? $0.resourceValues(forKeys: [.isRegularFileKey]).isRegularFile) == true
    }.sorted { $0.lastPathComponent < $1.lastPathComponent }
    guard !frames.isEmpty else { throw MaskError.noFrames }

    try files.createDirectory(at: output, withIntermediateDirectories: true)
    guard try files.contentsOfDirectory(atPath: output.path).isEmpty else {
        throw MaskError.outputNotEmpty
    }

    let context = CIContext()
    let grayscale = CGColorSpaceCreateDeviceGray()
    let request = VNGenerateForegroundInstanceMaskRequest()
    var emptyFrames = 0

    for frame in frames {
        guard let inputFrame = CIImage(contentsOf: frame) else {
            throw MaskError.unreadableFrame(frame.lastPathComponent)
        }
        let handler = VNImageRequestHandler(ciImage: inputFrame, orientation: .up)
        try handler.perform([request])

        let mask: CIImage
        if let result = request.results?.first, !result.allInstances.isEmpty {
            let pixels = try result.generateScaledMaskForImage(
                forInstances: result.allInstances, from: handler
            )
            mask = CIImage(cvPixelBuffer: pixels, options: [.colorSpace: NSNull()])
        } else {
            mask = CIImage(color: .black).cropped(to: inputFrame.extent)
            emptyFrames += 1
            fputs("No foreground detected in \(frame.lastPathComponent); wrote an empty mask.\n", stderr)
        }
        try context.writePNGRepresentation(
            of: mask, to: output.appendingPathComponent(frame.lastPathComponent),
            format: .L8, colorSpace: grayscale
        )
    }

    print("Wrote \(frames.count) masks (\(emptyFrames) without detected foreground).")
}

do {
    let args = CommandLine.arguments
    guard args.count == 3 else { throw MaskError.usage }
    guard #available(macOS 14.0, *) else {
        fputs("macOS 14 or later is required.\n", stderr)
        exit(EXIT_FAILURE)
    }
    try generateMasks(
        input: URL(fileURLWithPath: args[1], isDirectory: true),
        output: URL(fileURLWithPath: args[2], isDirectory: true)
    )
} catch {
    fputs("\(error.localizedDescription)\n", stderr)
    exit(EXIT_FAILURE)
}
